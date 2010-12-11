var pm = {
    status: { position: {} },
    
    init: function() {
        // Find current location
        geo.getPosition();    
        setInterval(function() { geo.updatePosition(); }, 3000);
                
        navigator.geolocation.watchPosition(geo.updatePosition);    
    
        $('#challenges').live('pageshow',function(event, ui) { pm.updateChallenges(); });
        
        $('#challenge-progress').live('pageshow',function(event, ui) { pm.showMap(); });  
    },
    
    updateChallenges: function() {
        var challenges = routing.getChallenges(),
            thumbSize = '150x150';
                        
        console.log(challenges);
        var html = '<ul data-role="listview">';
        $.each(challenges, function(i, val) {
            html += '<li>' 
				  + '<img src="http://maps.google.com/maps/api/staticmap?center='+val.latitude+','+val.longitude+'&zoom=15&size='+thumbSize+'&format=png&maptype=roadmap&sensor=false" />'
				  + '<h3><a href="index.html">'+val.name+'</a></h3>'
				  + '<p>Distance: '+val.distance+'</p>'
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


