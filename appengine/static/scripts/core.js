var pm = {
    status: { position: {}, challenge: {} },   
    data: { docks: {} },
    
    init: function() {
        // Find current location
        geo.getPosition();    
        geo.updatePosition(); 
        setInterval(function() { geo.updatePosition(); }, 10000);
                
        navigator.geolocation.watchPosition(geo.updatePosition);    
    
        $('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });    
        $('#challenge-progress').live('pageshow',function(event, ui) { pm.showMap(); });
        $('#challenge-finish').live('pageshow',function(event, ui) { pm.finishChallenge(event, ui); });
        $('#challenge-start-button').live('click',function() { 
            alert('start challenge');
        });
        
        $('#challenges .destinations a').live('click',function() { 
            var dockId = $(this).parents('li').attr('id').replace('dock-',''); 
            pm.status.challenge.destination = pm.data.docks[dockId];        
        });
        
        routing.updateBikeStatsFeedCallback = pm.updateChallenges;
    },
    
    updateChallenges: function() {
        var challenges = routing.getChallenges(),
            startThumbSize = '150x150',
            thumbSize = '150x150';
                         
        var html  = '<img src="http://maps.google.com/maps/api/staticmap?center='+challenges.start.latitude+','+challenges.start.longitude+'&zoom=15&size='+startThumbSize+'&format=png&maptype=roadmap&sensor=false" />'
				  + '<h2>Start Point - '+challenges.start.name+'</h2>'
				  + '<p class="ui-li-desc">Distance: <strong>'+Math.round(challenges.start.distance*100)/100+'km</strong></p>'
				  + '<p class="ui-li-desc">Bikes available: <strong>'+challenges.start.bikesAvailable+'</strong></p>'
			      + '</li>';
			      
			      //alert(html);
        //$('#challenges [data-role="content"]').html(html); 
        $('#challenges .start').html(html);    
        
        html = '<ul data-role="listview" class="destinations">';
        $.each(challenges.destinations, function(i, val) {
            var distance = Math.round(val.distance*100)/100;
            html += '<li id="dock-'+val.ID+'">' 
				  + '<img src="http://maps.google.com/maps/api/staticmap?center='+val.latitude+','+val.longitude+'&zoom=15&size='+thumbSize+'&format=png&maptype=roadmap&sensor=false" />'
				  + '<h3><a href="#challenge-start" data-rel="dialog" data-transition="slideup">'+val.name+'</a></h3>'
				  + '<p>Distance: <strong>'+distance+'km</strong>&nbsp;&nbsp;&nbsp;Empty slots: <strong>'+val.emptySlots+'</strong></p>'
			      + '</li>';            
        });
        html += '</ul>';

        //console.log(html);
        $('#challenges [data-role="content"]').html(html);
        
        $('#challenges .destinations').listview();
        
        // Set globals
        pm.status.challenge.start = challenges.start;
    },
    
    startChallenge: function(destinationDockId) {
    	var postData = {
    		from_id: pm.status.challenge.start.ID,
    		to_id: pm.status.challenge.destination.ID,
    		score: 10,
    		render: json	
    	}
    	$.post('/challenge/start', postData, function(data) {

        });            
    },
    
    showMap: function() {
        var cloudmade = new CM.Tiles.CloudMade.Web({key: 'c8a3643e0bb842b4a4491d0b96754cff', styleId: 24509});
        var map = new CM.Map('map', cloudmade);
        var startPoint = new CM.LatLng(pm.status.position.lat, pm.status.position.lon);
        var endPoint = new CM.LatLng(pm.status.position.lat, pm.status.position.lon);
        
        map.setCenter(startPoint, 16);
        
        var directions = new CM.Directions(map, 'panel', 'c8a3643e0bb842b4a4491d0b96754cff');

        var waypoints = [startPoint, endPoint];
        directions.loadFromWaypoints(waypoints);
    },
    
    finishChallenge: function(event, ui) {
    	console.log("test", event);
    	console.log("test", ui);
    	// Calculate score
    	var score = pm.calculateScores();
    	
    	// Post scores
    	var action = "challenge/complete";
    	var postData = {
    		from_id: 1,
    		to_id: 2,
    		score: 10,
    		render: json	
    	}
    	var node = $(this);

    	$.post(action, postData, function(data) {
    		// Update scores
    		
    		
    		// Choose random Boris quote and image
        });
    },
    
    calculateScores: function(start, end, distance) {
    	var p1 = ((start.totalSlots - start.emptySlots)/start.totalSlots) * 100; // Start station fullness percentage
    	var p2 = ((end.totalSlots - end.emptySlots)/end.totalSlots) * 100;// End station fullness percentage	
    	var f = p1 - p2; // Fullness factor
    	var D = 10; // Distance factor
    	
    	return score = distance * D * f;
    }

};

$(document).ready(function() { pm.init(); });


