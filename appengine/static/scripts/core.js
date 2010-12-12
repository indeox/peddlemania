var pm = {
    status: { position: {} },   
    
    init: function() {
        // Find current location
        geo.getPosition();    
        //setInterval(function() { geo.updatePosition(); }, 3000);
                
        navigator.geolocation.watchPosition(geo.updatePosition);    
    
        $('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });    
        $('#challenge-progress').live('pageshow',function(event, ui) { pm.showMap(); });
        $('#challenge-finished').live('pageshow',function(event, ui) { pm.finishChallenge(); });
        //$('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });
        
        routing.updateBikeStatsFeedCallback = pm.updateChallenges;
    },
    
    updateChallenges: function() {
        var challenges = routing.getChallenges(),
            thumbSize = '150x150';
                        
        
        var html  = '<ul data-role="listview" data-theme="a">'                
				  + '<img src="http://maps.google.com/maps/api/staticmap?center='+pm.status.position.latitude+','+pm.status.position.longitude+'&zoom=15&size='+thumbSize+'&format=png&maptype=roadmap&sensor=false" />'
				  + '<h3>asd</h3>'
				  + '<p>Distance: <strong>'+'km</strong></p>'
				  + '<p>Empty slots: <strong>'+'</strong></p>'
			      + '</li>';
			      + '</ul>';
			      
			      //alert(html);
        //$('#challenges .origin').html(html);
        //$('#challenges .origin ul').listview();    
        
        html = '<ul data-role="listview">';
        $.each(challenges, function(i, val) {
            var distance = Math.round(val.distance*100)/100;
            html += '<li>' 
				  + '<img src="http://maps.google.com/maps/api/staticmap?center='+val.latitude+','+val.longitude+'&zoom=15&size='+thumbSize+'&format=png&maptype=roadmap&sensor=false" />'
				  + '<h3><a href="#challenge-start" data-rel="dialog" data-transition="slideup">'+val.name+'</a></h3>'
				  + '<p>Distance: <strong>'+distance+'km</strong></p>'
				  + '<p>Empty slots: <strong>'+val.emptySlots+'</strong></p>'
			      + '</li>';            
        });
        html += '</ul>';

        console.log(html);
        $('#challenges [data-role="content"]').html(html);
        $('#challenges ul').listview();    
    },
    
    showMap: function() {
        var cloudmade = new CM.Tiles.CloudMade.Web({key: 'c8a3643e0bb842b4a4491d0b96754cff', styleId: 8909});
        var map = new CM.Map('map', cloudmade);
        var startPoint = new CM.LatLng(pm.status.position.lat, pm.status.position.lon);
        var endPoint = new CM.LatLng(pm.status.position.lat, pm.status.position.lon);
        
        map.setCenter(startPoint, 16);
        
        var directions = new CM.Directions(map, 'panel', 'c8a3643e0bb842b4a4491d0b96754cff');

        var waypoints = [startPoint, endPoint];
        directions.loadFromWaypoints(waypoints);
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


