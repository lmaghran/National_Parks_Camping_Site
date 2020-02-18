<script>
$('#select-np').on('submit', (evt) => {
  evt.preventDefault();

  const selectedStart = $('#start-date').val();
  const selectedEnd = $('#end-date').val();
  const selectedNp = $('#rec_area').val();


  $.ajax({
    url: `/api/np_selected`,
    type: "get",
    dataType: "json",
    data: {
      "start-date": selectedStart,
      "end-date": selectedEnd,
      "rec_area": selectedNp
    },
    success: console.log(selectedStart);
    }})

    ;
  

</script>