function ajaxandmap(result) 
    {
      Object.keys(result).forEach(function(item)
      {
        if ((String(item)) !== 'mapping_list'){

        let campground = $("<li><h2 id='replacement'><a href=https://www.recreation.gov/camping/campgrounds/"+ String(result[item]['campground_id']) +">"+ String(item) +'</a></li>')
        $('#replacement').append(campground);

        if (result[item]['availibility_data']!= null)
        { 
         // value

          for (campsite of result[item]['availibility_data'])
          {
        
          let campList = $("<li><h5 id='campsite-list'><a href='https://www.recreation.gov/camping/campsites/" + String(campsite['campsite_id']) + "'>" + String(campsite["site"]) +"(availible site)" +'</a></li>')
            $('#replacement').append(campList);
          }
        }

        else
        {
          let emptyCampsite = $('<li><h5>' + "No campsites available for these dates at this campground" +'</li>')
          $('#replacement').append(emptyCampsite);
        }

      }
      });


console.log("after looping")
  $('#map').remove();
  let createmapdiv = $('<div id="map"></div>')
  $('#mapdiv').append(createmapdiv);
  initMap()


//   function initMap() {
//     console.log("ajax init map function call");

//     //// map options
//   let options = {
//   zoom: 4,
//   center: {lat: 39.8283, lng: -98.5795}
//     }

//   ///new map
//   let map = new google.maps.Map(document.getElementById('map'), options);

// //to add markers to map
// function addMarker(params){
//   var marker= new google.maps.Marker({
//     position: params.coords,
//     map: map

//     });

//   var infoWindow= new google.maps.InfoWindow({
//     content: params.content
//   });

//   marker.addListener('click', function(){
//     infoWindow.open(map, marker)
//   });

// }



// /// loop through markers
// $.get("/api/all_campground_geodata", function(data){
//     for (var i = 0; i<data.length; i++){
//     addMarker({coords:{lat:data[i].lat, lng:data[i].long},
//               content: data[i].campground_name
// });
// }
// });
// }
};


$('#select-np').on('submit', (evt) => {
  evt.preventDefault();
  console.log("Prevented default")

  const selectedStart = $('#start-date').val();
  const selectedEnd = $('#end-date').val();
  const selectedNp = $('#npList').val();

  $.ajax(

  {
    url: `/api/np_selected`,
    type: "get",
    dataType: "json",
    data: 
    {
      "start-date": selectedStart,
      "end-date": selectedEnd,
      "rec_area": selectedNp
    },
    success: (result) => {ajaxandmap(result)}

  });
});


