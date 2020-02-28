var map = null;
var markers = [];

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
    content: params.content,

    });

  var infoWindow= new google.maps.InfoWindow({
    content: params.content
  });

  marker.addListener('click', function(){
    infoWindow.open(map, marker)
  });

  return marker
}

// setMap(null)





$.get("/api/np_selected", function(data){
    for (campground of data.mapping_list){
      if (campground.availibility === 'Availible for these dates'){
      var fill = "#0F9D58";
      }
      else if (campground.availibility === 'Not availible for these dates'){
      var fill = "#DB4437";
      }
      else if (campground.availibility === 'Availibility Unknown'){
      var fill= "#79c1f1";
      }

    let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
    fillOpacity: 0.4, strokeWeight: 0.4}

      marker = addMarker({coords:{lat:campground.lat, lng:campground.long},
          content: campground.campground_name, icon: icon, map:map});

      markers.push(marker)

    }
    // console.log(markers)

});

}

// let fill= "#79c1f1"

// let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
//     fillOpacity: 0.4, strokeWeight: 0.4}

// function addMarker(params){
//   var marker= new google.maps.Marker({
//     position: params.coords,
//     map:map,
//     icon: params.icon,
//     content: params.content

//     });

// }

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


  console.log("after looping");
  console.log(map);
  console.log(result)

  for (marker of markers){
    marker.setMap(null)
};

  for (campground of result.mapping_list){
      if (campground.availibility === 'Availible for these dates'){
      var fill = "#0F9D58";
      }
      else if (campground.availibility === 'Not availible for these dates'){
      var fill = "#DB4437";
      }
      else if (campground.availibility === 'Availibility Unknown'){
      var fill= "#79c1f1";
      }

      let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
        fillOpacity: 0.4, strokeWeight: 0.4}

      marker = new google.maps.Marker({
                    position: {lat:campground.lat, lng:campground.long},
                    map:map,
                    icon: {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
                    fillOpacity: 0.4, strokeWeight: 0.4},
                    content:campground.campground_name
    });

      markers.push(marker)


      // marker = addMarker({coords:{lat:result.mapping_list[i].lat, lng:result.mapping_list[i].long},
      //     content: result.mapping_list[i].campground_name, icon: icon, map:map});

      marker.setMap(map)
  }
  };
      // for (var i = 0; i< data.mapping_list.length; i++){
      // if (data.mapping_list.availibility_data === 'Availible for these dates'){
      //   fill = "#0F9D58";
      // }
      // else if (data.mapping_list.availibility_data === 'Not availible for these dates'){
      //   fill = "#DB4437";
      // }
      // else if (data.mapping_list.availibility_data === 'Availibility Unknown'){
      //   let fill= "#79c1f1";
      // }

      // marker = addMarker({coords:{lat:data.mapping_list[i].lat, lng:data.mapping_list[i].long},
      //     content: data.mapping_list[i].campground_name, icon: icon, map:map});

      // markers.push(marker)


  // }

  // initMap()
// };



////AJAX Call after user clicks
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
