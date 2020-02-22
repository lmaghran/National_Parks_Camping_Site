
$('#select-np').on('submit', (evt) => 
{
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
    success: function(result) 
    {
      Object.keys(result).forEach(function (item) 
      {
        console.log(result[item]);

        let campground = $("<li><h2 id='replacement'><a href=https://www.recreation.gov/camping/campgrounds/"+ String(result[item]['campground_id']) +">"+ String(item) +'</a></li>')
        $('#replacement').append(campground);
        console.log(String(result[item]['campground_id']))


        if (result[item]['availibility_data']!= null)
        { 
         // value

          for (campsite of result[item]['availibility_data'])
          {
            console.log(campsite);
        
          let campList = $("<li><h5 id='campsite-list'><a href='https://www.recreation.gov/camping/campsites/" + String(campsite['campsite_id']) + "'>" + String(campsite["site"]) +"(availible site)" +'</a></li>')
            $('#replacement').append(campList);
          }
        }

        else
        {
          let emptyCampsite = $('<li><h5>' + "No campsites available for these dates at this campground" +'</li>')
          $('#replacement').append(emptyCampsite);
        }
      });
    }});
});