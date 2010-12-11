var pm = {
    status: { position: {} },   
    
    init: function() {
        // Find current location
        geo.getPosition();    
        //setInterval(function() { geo.updatePosition(); }, 3000);
                
        navigator.geolocation.watchPosition(geo.updatePosition);    
    
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
        $('#challenges .list').html(html);
        $('#challenges .list ul').listview();    
    }

};

$(document).ready(function() { pm.init(); });


