routing = {
	HARD: 3,
	MEDIUM: 2, 
	EASY: 1,
	
	data: [],
	currentTarget: null,
	updateBikeStatsFeedCallback: null,
	
	makeCurrentTarget: function (dock) {
		this.currentTarget = dock;
	},
	
	periodicBikeTargetCheck: function() {
		if (!this.currentTarget || this.data) {
			return;
		}
		
		for (var i = 0; i < this.data.length; i++) {
			if (this.data[i].ID === this.currentTarget.ID) {
				if (this.data[i].emptySlots == 0) {
					return { status: 10, message: 'No free place to park your bike' };
				} else if (this.data[i].emptySlots < 2) {
					return { status: 20, message: 'Limited free places to park your bike' };
				}
			}
		}
		
	},
	
	updateBikeStatsFeed: function(callback) {
		/* check to see if network is reachable */
		var apiEndpoint = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%3D'http%3A%2F%2Fapi.bike-stats.co.uk%2Fservice%2Frest%2Fbikestats'&format=json&diagnostics=true&callback=?";
		apiEndpoint = "/scripts/yahoo_response.json";
		$.getJSON(apiEndpoint, function(data) {
		    routing.parseBikeStatsFeed(data);
            if (callback) {
                this.updateBikeStatsFeedCallback = callback;
            }		
		});
	},
	
	parseBikeStatsFeed: function (request) {
		routing.data = request.query.results.dockStationList.dockStation;
		if (this.updateBikeStatsFeedCallback) {
			this.updateBikeStatsFeedCallback(request);
		}
	},
	
	/*
	 * @param difficulty 1-3  --  1 is easiest, 3 is hardest route.
	 * @returns {"ID":"32", 
	 *					"latitude":"51.52469624",
	 *					"longitude":"-0.084439283", 
	 *					"name":"Leonard Circus , Shoreditch",
	 *					"temporary":"false",
	 *					"emptySlots":"17",
	 *					"bikesAvailable":"4"}
	 */
	getChallenges: function() {
	
		if (this.data == null) {
			return [];
		}
	
	    //console.log(pm.status.position.lat, pm.status.position.lon);
	    
		var bikeArray = new Array;
		for (var i = 0; i < this.data.length; i++) {
			var bikeNode = this.data[i];
			bikeNode.distance = new Number(geo.getDistance(pm.status.position.lat, pm.status.position.lon, bikeNode.latitude, bikeNode.longitude));
			var availScore = new Number(bikeNode.bikesAvailable / bikeNode.emptySlots);
			bikeNode.score = bikeNode.distance+ availScore.toFixed(1);
			bikeNode.h = 0;
			bikeNode.g = 0;
			bikeNode.f = 0;
			bikeArray.push(bikeNode);
			
    		pm.data.docks[bikeNode.ID] = bikeNode;
		}
	
		
		bikeArray.sort(function(a,b) {
										if (a.score > b.score) {
											return 1;
										} else if (b.score > a.score) {
											return -1;
										} else {
											return 0;
										}
							}
		);
		
		var challenges = {
		    start: bikeArray[0],
		    destinations: {
                easy: bikeArray[Math.round(bikeArray.length * 0.5) ],
                medium: bikeArray[Math.round(bikeArray.length * 0.75) ],
                hard: bikeArray[bikeArray.length-1]				    
		    }
		}
		
		return challenges;
		
		if (difficulty == this.MEDIUM) {
			return bikeArray[Math.round(bikeArray.length / 2) ];
		} else if (difficulty == this.HARD) {
			return bikeArray[bikeArray.length-1];
		} else {
			//easy
			return bikeArray[0];
		}
	}

}





var astar = {
	search: function( start, end) {
		//astar.init(grid);
 
		var openList   = [];
		var closedList = [];
		openList.push(start);
 
		while(openList.length > 0) {
 
			// Grab the lowest f(x) to process next
			var lowInd = 0;
			for(var i=0; i<openList.length; i++) {
				if(openList[i].f < openList[lowInd].f) { lowInd = i; }
			}
			var currentNode = openList[lowInd];
            //console.log(currentNode);
			// End case -- result has been found, return the traced path
			if(currentNode.ID == end.ID) {
				var curr = currentNode;
				var ret = [];
				while(curr.parent) {
					ret.push(curr);
					curr = curr.parent;
				}
				return ret.reverse();
			}
 
			// Normal case -- move currentNode from open to closed, process each of its neighbors
			openList.removeGraphNode(currentNode);
			closedList.push(currentNode);
			var neighbors = astar.neighbors(currentNode);

			for(var i=0; i<neighbors.length;i++) {
				var neighbor = neighbors[i];
				if(closedList.findGraphNode(neighbor)) { // || neighbor.isWall()) {
					// not a valid node to process, skip to next neighbor
					console.log('not a valid node to process, skip to next neighbor');
					continue;
				}
 
				// g score is the shortest distance from start to current node, we need to check if
				//	 the path we have arrived at this neighbor is the shortest one we have seen yet
				var gScore = currentNode.h ; // 1 is the distance from a node to it's neighbor
				var gScoreIsBest = false;
 
 
				if(!openList.findGraphNode(neighbor)) {
					// This the the first time we have arrived at this node, it must be the best
					// Also, we need to take the h (heuristic) score since we haven't done so yet
 
					gScoreIsBest = true;
					neighbor.h = fitness(currentNode, neighbor, end);
					openList.push(neighbor);
				}
				else if(gScore < neighbor.h) {
					// We have already seen the node, but last time it had a worse g (distance from start)
					gScoreIsBest = true;
				}
 
			console.log(); 
				if(gScoreIsBest) {
					// Found an optimal (so far) path to this node.	 Store info on how we got here and
					//	just how good it really is...
					neighbor.parent = currentNode;
					neighbor.g = gScore;
					neighbor.f = neighbor.g + neighbor.h;
					neighbor.debug = "F: " + neighbor.f + "<br />G: " + neighbor.g + "<br />H: " + neighbor.h;

				}
			}
		}
 
		// No result was found -- empty array signifies failure to find path
		return [];
	},

	neighbors: function(node) {
	
		var ret = [];

		var bikeArray = new Array;
		for (var i = 0; i < routing.data.length; i++) {
			var bikeNode = routing.data[i];
			bikeNode.distance = new Number(geo.getDistance(node.latitude, node.longitude, bikeNode.latitude, bikeNode.longitude));
			var availScore = new Number(bikeNode.bikesAvailable / bikeNode.emptySlots);
			bikeNode.score = bikeNode.distance+ availScore.toFixed(1);
			bikeArray.push(bikeNode);
		}
		
		bikeArray.sort(function(a,b) {
										if (a.score > b.score) {
											return 1;
										} else if (b.score > a.score) {
											return -1;
										} else {
											return 0;
										}
							}
		);

		ret.push(bikeArray[bikeArray.length/2]);
		ret.push(bikeArray[(bikeArray.length/2)+1]);
		ret.push(bikeArray[(bikeArray.length/2)+2]);
		ret.push(bikeArray[(bikeArray.length/2)+3]);

		console.log(ret);
		return ret;
	}
};

Array.prototype.findGraphNode = function(obj) {
	for(var i=0;i<this.length;i++) {
		if(this[i].ID == obj.ID) { return this[i]; }
	}
	return false;
};
Array.prototype.removeGraphNode = function(obj) {
	for(var i=0;i<this.length;i++) {
		if(this[i].ID == obj.ID) { this.splice(i,1); }
	}
	return false;
};