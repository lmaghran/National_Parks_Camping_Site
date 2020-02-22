function getrequest(LAT, LNG){
 let N_name="";
 const KEY = “YOUR-KEY”;
 let url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${LAT},${LNG}&key=${KEY}`;
        return fetch(url)
        .then(response => response.json())
        .then(data => {
         let parts = data.results[0].address_components;
         parts.forEach(part => {
          if (part.types.includes(“THE FIELD THAT YOU NEED EXP: street_number
”)) {
           
           N_name=part.long_name;
          }
         });
         return N_name;
        })
        .catch(err => console.warn(err.message)); 
}


 // Ajax call to get place information from server.py db, make markers, add markers to map
$.get('/api', {map_id : map_id}, markerCreation);
function markerCreation(response) {
  for (const item of response) {
    userMarkers.push(new google.maps.Marker({
      position: {
        lat: item.lat,
        lng: item.long
      },
      title: place.title,
      address: place.address,
      website: place.website,
      icon: {
      url: '/static/img/map_icon_red_black.png', 
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(20, 20)
    },
    map: map,
    }));
  }


const get_campsite_geodata= 

$.ajax(
  {
    url: `/api/campground/geodata`,
    type: "get",
    dataType: "json",
    success: function(result) 
    {
      Object.keys(result).forEach(function (item) 
      {
      console.log(result[item]);
    });
}};

