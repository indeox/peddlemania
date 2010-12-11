var pm = {
    status: { position: {} },   
    
    init: function() {
        // Find current location
        geo.getPosition();    
        //setInterval(function() { geo.updatePosition(); }, 3000);
                
        navigator.geolocation.watchPosition(geo.updatePosition);    
    
        $('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });    
        $('#challenge-progress').live('pageshow',function(event, ui) { pm.showMap(); });  
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
    	alert("map");
    	var latitude = (position.coords.latitude).toFixed(6);
		var longitude = (position.coords.longitude).toFixed(6);
		
		var myOptions = 
		{
			center: new google.maps.LatLng(latitude,longitude),
			zoom: 16,
    		mapTypeId: google.maps.MapTypeId.HYBRID
		};
  		
		var map = new google.maps.Map(document.getElementById("map"), myOptions);    	

    }

};

$(document).ready(function() { pm.init(); });


