
var map = null;

function initMap(marker_func) {
  console.log("google map init map function");

  //// map options
  var options = {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}
  }

  ///new map
  map = new google.maps.Map(document.getElementById('map'), options);
  console.log(map)

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


$.get("/api/np_selected", function(data){
    for (var i = 0; i< data.mapping_list.length; i++){
      if (data.mapping_list.availibility_data === 'Availible for these dates'){
        fill = "#0F9D58";
      }
      else if (data.mapping_list.availibility_data === 'Not availible for these dates'){
        fill = "#DB4437";
      }
      else if (data.mapping_list.availibility_data === 'Availibility Unknown'){
        let fill= "#79c1f1";
      }
    addMarker({coords:{lat:data.mapping_list[i].lat, lng:data.mapping_list[i].long},
              content: data.mapping_list[i].campground_name,
              icon: icon});
}
});
}

