var pm = {
    

};

$(document).ready(function() {
    // Init    
    pm.status = { position: {} };
    
    
    routing.updateBikeStatsFeedCallback = function() {
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
    };
    
    
    // Find current location
    geo.getPosition();    
    setInterval(function() { geo.updatePosition(); }, 3000);
            
    navigator.geolocation.watchPosition(geo.updatePosition);    


    $('#challenges').live('pageshow',function(event, ui){
      //alert('This page was just hidden: '+ ui.prevPage);
    });
    
});


