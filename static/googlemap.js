function initMap() {
  console.log("google map init map function");

  var zoom = 4
  var center= {lat: 39.8283, lng: -98.5795}

  //// map options
  var options = {
    zoom: zoom,
    center: center
  }

  ///new map
  var map = new google.maps.Map(document.getElementById('map'), options);



//to add markers to map
function addMarker(params){
  var marker= new google.maps.Marker({
    position: params.coords,
    map:map,
    icon: params.icon,

    });

  var infoWindow= new google.maps.InfoWindow({
    content: params.content
  });

  marker.addListener('click', function(){
    infoWindow.open(map, marker)
  });

}

let fill= "#79c1f1"

/// loop through markers
$.get("/api/all_campground_geodata", function(data){
    for (var i = 0; i<data.length; i++){
    addMarker({coords:{lat:data[i].lat, lng:data[i].long},
              content: data[i].campground_name,
              icon: {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
                      fillOpacity: 0.4, strokeWeight: 0.4}});
}
});
}