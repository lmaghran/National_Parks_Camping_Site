
function initMap() {

  //// map options
  var options = {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}
  }

  ///new map
  var map = new google.maps.Map(document.getElementById('map'), options);


//array of markers
var markers = [
{coords: {lat:42.4668, lng: -70}}, {coords: {lat:42, lng: -70}}

];




function addMarker(params){
  var marker= new google.maps.Marker({
    position: params.coords,
    content: params.content,
    map:map

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




// // Create a <script> tag and set the USGS URL as the source.
// var script = document.createElement('script');
// // This example uses a local copy of the GeoJSON stored at
// // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
// script.src = '/api/all_campground_geodata';
// console.log(script.src)
// document.getElementsByTagName('head')[0].appendChild(script);
// }


// // Loop through the results array and place a marker for each
// // set of coordinates.
// window.result_list = function(results) {
// for (var i = 0; i < results.length; i++) {
//   console.log("at this step!!");
//   var coords = results.features[i].geometry.coordinates;
//   var latLng = new google.maps.LatLng(coords[1],coords[0]);
//   var marker = new google.maps.Marker({
//     position: latLng,
//     map: map
//   });
// }
// }

//Add marker function

// function addMarker(coordinates){

//     var marker= new google.maps.Marker({
//         position: coordinates,
//         map:map
//     });
// }
