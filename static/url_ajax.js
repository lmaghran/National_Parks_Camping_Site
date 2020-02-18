"use strict";

// $('#select-np').on('submit', (evt) => {
//   evt.preventDefault();

//   const selectedNp = $('#rec_area').val();
//   const startDate = $('#start-date').val();
//   const endDate = $('#end-date').val();
//   availibility_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'


//   $.get(`/api/human/${selectedId}`, (res) => {
//     $('#fname').html(res.fname);
//     $('#lname').html(res.lname);
//     $('#email').html(res.email);
//   });
// });

function ajax_qry (availibility_url_list){
    for (url of availibility_url_list) {
        console.log(url);
    }
}