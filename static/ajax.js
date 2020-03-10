var map = null;
var markers = [];

//Adds markers and content window to map
function addMarker(params){
  var marker= new google.maps.Marker({
    position: params.coords,
    map:map,
    icon: params.icon,
    type: params.type

    });

  var contentString = 
      '<div id="content">'+
      '<div id="siteNotice">'+
      params.content+'<br>'+
      params.available+ "<br>"+
      '<a href=https://www.recreation.gov/camping/campgrounds/'+
      params.fac_id +" target='_blank'>"+
      "Go to reservation website"+
      '</a>'+'</div>';


  var infoWindow= new google.maps.InfoWindow({
    content: contentString
  });

  marker.addListener('click', function(){
    infoWindow.open(map, marker)
  });

  return marker
}

//This function creates the map and adds it to the map object above
function initMap(){
  console.log("google map init map function");

  //// map options
  var options = {
    zoom: 4.5,
    center: {lat: 39.8283, lng: -98.5795},
    styles: [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#ebe3cd"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#523735"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "administrative",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#c9b2a6"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#dcd2be"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#ae9e90"
      }
    ]
  },
  {
    "featureType": "landscape.natural",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "landscape.natural.landcover",
    "stylers": [
      {
        "saturation": -40
      },
      {
        "lightness": 30
      },
      {
        "weight": 2
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#93817c"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#a5b076"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels",
    "stylers": [
      {
        "saturation": 100
      },
      {
        "lightness": 10
      },
      {
        "weight": 3.5
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#447530"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#fdfcf8"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f8c967"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#e9bc62"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e98d58"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#db8555"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#806b63"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#8f7d77"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#ebe3cd"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#b9d3c2"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#92998d"
      }
    ]
  }
]


  }

  ///new map
  map = new google.maps.Map(document.getElementById('map'), options);

//API call to add the initial markers to the map
$.get("/api/np_selected", function(data){
    for (campground of data.mapping_list){
      if (campground.availibility.startsWith('Availible')){
        var fill = "#0F9D58";
        var type = "Available"
      }

      else if (campground.availibility.startsWith("Not")){
      var fill = "#DB4437";
      var type = "Not available";
      }

      else if (campground.availibility === 'Availibility Unknown'){
      var fill = "#79c1f1";
      var type = 'Availability Unknown';
      }

      // console.log(campground.campground_name);

    let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
    fillOpacity: 0.4, strokeWeight: 0.4}

    marker = addMarker({coords:{lat:campground.lat, lng:campground.long},
            content: campground.campground_name, available: campground.availibility,
            fac_id:campground.facility_id,
           icon: icon, map:map, type: type});

    markers.push(marker)

    }
});
}


//Function for dom manipulation and addinng points to the map
function ajaxandmap(result) {
    ///Adds campgrounds to the dom with links

      $('#replacement').empty()

      let nationalParkname= "<h5 id='replacement'><strong>" + String(result['rec_area'])+ "</strong></h5>"
      $('#replacement').append(nationalParkname);

      let datesStayed= "<h5> Check-in : " + String(result['dates'][0]) + "<br>" + " Check-out : " + String(result['dates'][1])+"</h5>"
      $('#replacement').append(datesStayed);

      console.log(String(result['dates']));

      Object.keys(result).forEach(function(item) {

        if (((String(item)) !== 'mapping_list') && ((String(item)) !== 'rec_area') && ((String(item)) !== 'dates')){

        if (result[item]['availibility_data']!= null){

          let campground = $("<li><p id='replacement'><strong><a href=https://www.recreation.gov/camping/campgrounds/"+ String(result[item]['campground_id']) +">"+ String(item) +'</a></strong></p></li>')
          $('#replacement').append(campground);

          // console.log(result[item]['availibility_data']);

          let availCampsite = $('<p> There are ' + String(result[item]['availibility_data'].length)  +" sites available at this campground, click to book. </p>")
          $('#replacement').append(availCampsite);

        //   // for (campsite of result[item]['availibility_data']){
        
        //   // let campList = $("<li><h5 id='campsite-list'><a href='https://www.recreation.gov/camping/campsites/" + String(campsite['campsite_id']) + "'>" + String(campsite["site"]) +"(availible site)" +'</a></li>')
        //   //   $('#replacement').append(campList);
        //   // }
        }

        else {

          let campground = $("<li><p id='replacement'><strong>" + String(item) +'</strong></p></li>')
          $('#replacement').append(campground);

          let emptyCampsite = $('<p>' + "No campsites available for these dates at this campground" +'</p>')
          $('#replacement').append(emptyCampsite);
        }

      }

      });

  //remove markers from map
  for (marker of markers){
    marker.setMap(null)
    };

  //adds different colors to the map based on availibility
  for (campground of result.mapping_list){
      if (campground.availibility.startsWith('Availible')){
      var fill = "#0F9D58";
      var fillOpacity= 1;
      map.setCenter({lat:campground.lat, lng:campground.long});

      }
      else if (campground.availibility.startsWith("Not")){
      var fill = "#DB4437";
      var fillOpacity= 1;
      map.setCenter({lat:campground.lat, lng:campground.long});
      }
      else if (campground.availibility === 'Availibility Unknown'){
      var fill= "#79c1f1";
      var fillOpacity= .4;
      }

      let icon= {path: google.maps.SymbolPath.CIRCLE, scale: 8.5, fillColor: fill,
        fillOpacity: fillOpacity, strokeWeight: 0.4};

      var marker = addMarker({coords:{lat:campground.lat, lng:campground.long},
                              content: campground.campground_name, 
                              fac_id: campground.facility_id,
                              available: campground.availibility,
                              icon: icon, map:map});
    }
      map.setZoom(8)


};


////AJAX Call after user clicks the submit button
$('#select-np').on('submit',  (evt) => {
  evt.preventDefault();
  

  const selectedStart = $('#start-date').val();
  const selectedEnd = $('#end-date').val();
  const selectedNp = $('#npList').val();

  $.ajax( {
    url: `/api/np_selected`,
    type: "get",
    dataType: "json",
    data: {
      "start-date": selectedStart,
      "end-date": selectedEnd,
      "rec_area": selectedNp
    },
    success: (result) => {ajaxandmap(result)}

  });
});

////AJAX Call for the user clicking a national park
$('#np-info').on('click',  (evt) => {
  evt.preventDefault();

  const selectedNp = $('#npList').val();

  $.ajax( {
    url: `/api/np`,
    type: "get",
    data: {
    "rec_area": selectedNp
    },
    success: (result) => {
      // console.log(result);

      // console.log(result['latLong'])
      map.setCenter({lat:Number(result['latitude']), lng: Number(result['longitude'])});
      map.setZoom(8)

    // map.setCenter({result['latLong']});

    $('#nps-name').text(String(result['fullName']));
    // $('#nps-description').empty();
    $('#nps-description').text(String(result['description']));
    $('#nps-directions').text("Driving Directions: "+ String(result['directionsInfo']))
    $('#images').empty()
    for (img of result['images']){
        let image = $("<img class='image' src='"+ String(img['url']) + "' height='100px'><br>")
          $('#images').append(image);
    } 
    }
    });
  });