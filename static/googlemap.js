function initMap() {

  //// map options
  var options = {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}
  }

  ///new map
  var map = new google.maps.Map(document.getElementById('map'), options);


//to add markers to map
function addMarker(params){
  var marker= new google.maps.Marker({
    position: params.coords,
    map:map

    });

  var infoWindow= new google.maps.InfoWindow({
    content: params.content
  });

  marker.addListener('click', function(){
    infoWindow.open(map, marker)
  });

}

/// loop through markers
$.get("/api/all_campground_geodata", function(data){
    for (var i = 0; i<data.length; i++){
    addMarker({coords:{lat:data[i].lat, lng:data[i].long},
              content: data[i].campground_name
});
}
});
}
