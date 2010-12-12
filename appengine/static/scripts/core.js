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
        $('#challenges .destinations a').live('click',function() { 
            var dockId = $(this).parents('li').attr('id').replace('dock-',''); 
            pm.status.challenge.destination = pm.data.docks[dockId];        
        });    
        
        $('#challenge-progress').live('pageshow',function(event, ui) { pm.showMap(); });  
        
        
        //$('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });
        
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
    
    setChallenge: function(destinationDockId) {
        
    
    },
    
    showMap: function() {
    	alert("map");
    	//var latitude = (position.coords.latitude).toFixed(6);
		//var longitude = (position.coords.longitude).toFixed(6);
		
		var myOptions = 
		{
			center: new google.maps.LatLng(pm.status.position.latitude,pm.status.position.longitude),
			zoom: 16,
    		mapTypeId: google.maps.MapTypeId.ROADMAP
		};
  		
		var map = new google.maps.Map(document.getElementById("map"), myOptions);    	

    }

};

$(document).ready(function() { pm.init(); });


