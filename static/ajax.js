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
      params.availible+ "<br>"+
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


  var legend = document.getElementById('legend');
    // for (var key in icons) {
      // var type = icons[key];
      // var name = type.name;
      // var icon = type.icon;
      var div = document.createElement('div');
      div.innerHTML = '<img src="' + 'https://maps.google.com/mapfiles/kml/shapes/parking_lot_maps.png' + '"> ';
      legend.appendChild(div);
    

        map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);

  return marker
}

//This function creates the map and adds it to the map object above
function initMap(){
  console.log("google map init map function");

  //// map options
  var options = {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}

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
            content: campground.campground_name, fac_id:campground.facility_id,
           icon: icon, map:map, type: type});

    markers.push(marker)

    }
});
}


//Function for dom manipulation and addinng points to the map
function ajaxandmap(result) {
    ///Adds campgrounds to the dom with links

      let nationalParkname= "<h2 id='replacement'>" + String(result['rec_area'])+ "</h2>"
      $('#replacement').append(nationalParkname);

      let datesStayed= "<h3> Check-in : " + String(result['dates'][0]) + "<br>" + " Check-out : " + String(result['dates'][1])+"</h3>"
      $('#replacement').append(datesStayed);

      console.log(String(result['dates']));

      Object.keys(result).forEach(function(item) {

        if (((String(item)) !== 'mapping_list') && ((String(item)) !== 'rec_area') && ((String(item)) !== 'dates')){

        let campground = $("<li><h2 id='replacement'><a href=https://www.recreation.gov/camping/campgrounds/"+ String(result[item]['campground_id']) +">"+ String(item) +'</a></li>')
        $('#replacement').append(campground);

        if (result[item]['availibility_data']!= null){ 

          let availCampsite = $('<h3>' + "This campground is available for these dates, click to book." +'</h3>')
          $('#replacement').append(availCampsite);

        //   // for (campsite of result[item]['availibility_data']){
        
        //   // let campList = $("<li><h5 id='campsite-list'><a href='https://www.recreation.gov/camping/campsites/" + String(campsite['campsite_id']) + "'>" + String(campsite["site"]) +"(availible site)" +'</a></li>')
        //   //   $('#replacement').append(campList);
        //   // }
        }

        else {
          let emptyCampsite = $('<h5>' + "No campsites available for these dates at this campground" +'</h5')
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
                              availible: campground.availibility,

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
        let image = $("<img id='image' src='"+ String(img['url']) + "'width='500' height='200'><br>")
          $('#images').append(image);

        let caption = $("<div id='caption'>"+ String(img['caption']) + "</div>")
          $('#image').append(caption);

    } 
    }
    });
  });