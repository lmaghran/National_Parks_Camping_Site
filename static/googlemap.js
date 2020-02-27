function initMap(marker_func) {
  console.log("google map init map function");

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

  let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
      fillOpacity: 0.4, strokeWeight: 0.4}

/// loop through markers



$.get("/api/np_selected", function(data){
    for (var i = 0; i< data.mapping_list.length; i++){
    addMarker({coords:{lat:data.mapping_list[i].lat, lng:data.mapping_list[i].long},
              content: data.mapping_list[i].campground_name,
              icon: icon});
}
});
}