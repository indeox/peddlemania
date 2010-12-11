geo = {
    firstRun: true,
    updatePosition: function(position) {
        //console.log('update position');
        //pm.status.position.lat = position.coords.latitude;
        //pm.status.position.lon = position.coords.longitude;        
        pm.status.position.lat = 51.51333;
        pm.status.position.lon =  -0.088947;        

        pm.status.destination = {};
        pm.status.destination.lat = 51.51333;
        pm.status.destination.lon = -0.088947;        

        pm.status.destinationDistance = geo.getDistance(pm.status.position.lat, pm.status.position.lon, pm.status.destination.lat, pm.status.destination.lon);
     	pm.status.destinationBearing = geo.getBearing(pm.status.position.lat, pm.status.position.lon, pm.status.destination.lat, pm.status.destination.lon);

	    //$('distance').innerHTML = distance;
  	    //$('bearing').innerHTML = bearing;		
        //$('position').innerHTML = ''+bh.position[0]+','+bh.position[1];        
            
        if (geo.firstRun) {
            routing.updateBikeStatsFeed();
            setInterval(function(){ 
                routing.updateBikeStatsFeed(function() {  
                    //console.log(routing.getClosestBike(3)); 
                }); 
            }, 60000);
            geo.firstRun = false;
        }        
        //routing.getClosestBike(2);
        //console.log(routing.getClosestBike(3));
        
        /*
        setTimeout(function() { 
        			var route = astar.search( { ID: 0, latitude: bh.position[0], longitude: bh.position[1] },  bh.routing.getClosestBike(3)); 
        			var rstr = '';
        			for (var x in route) {
                        // console.log('<Placemark><name>' +route[x].name+'</name><Point><coordinates>'+route[x].longitude + ','+route[x].latitude+',0</coordinates></Point></Placemark>');
						rstr += route[x].longitude + ','+route[x].latitude+',2357,';
        				
        			}
        		console.log(rstr);
       	}, 6000);
       	*/
    },


	bearingTo: function(from, to) {
  		var lat1 = from.latitude * Math.PI / 180,
  			  lat2 = to.latitude *  Math.PI / 180;
	  	var dLon = (to.longitude-from.longitude) * Math.PI / 180;

  		var y = Math.sin(dLon) * Math.cos(lat2);
  		var x = Math.cos(lat1)*Math.sin(lat2) - Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
  		var bearing = Math.atan2(y, x);
  
  		return ((bearing * 180 / Math.PI) +360) % 360;
	},
	

	getPosition: function(callback) {
	    navigator.geolocation.getCurrentPosition(foundLocation, noLocation);	    
        function foundLocation(position) {
          pm.status.position.lat = position.coords.latitude;
          pm.status.position.lon = position.coords.longitude;          
          console.log('found loc ', position.coords.latitude, position.coords.longitude);
        }
        function noLocation() {
          pm.status.position.lat = 0;
          pm.status.position.lon = 0;          
          console.log('not found');          
        }
        
        if (callback) { callback; }
	},
	
    getBearing: function(lat1, lon1, lat2, lon2) {
        var y = Math.sin(lon2-lon1) * Math.cos(lat2);
        var x = Math.cos(lat1)*Math.sin(lat2) -
                Math.sin(lat1)*Math.cos(lat2)*Math.cos(lon2-lon1);
        //var brng = Math.atan2(y, x).toDeg();
        var bearing = (Math.atan2(y, x))* 180 / Math.PI;
        return bearing;
    },
    
    getDistance: function(lat1, lon1, lat2, lon2) {
        var R = 6371; // km
        var dLat = (lat2-lat1)*(Math.PI/180);
        var dLon = (lon2-lon1)*(Math.PI/180); 
        var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1*(Math.PI/180)) * Math.cos(lat2*(Math.PI/180)) * 
                Math.sin(dLon/2) * Math.sin(dLon/2); 
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
        var d = R * c;
        return d;
    }
}
