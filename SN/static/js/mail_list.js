// function update_ml(){

//     // var to_url = $('#mail_list').attr('data-to-url');
//     var to_url = $('#last10msgs').attr('data-to-url');
//     // console.log(to_url);
//     // console.log(from_url);

//     // var ajaxdata = {
//     //     from_url: from_url
//     // };

//     $.ajax({
//         // url: `/accounts/essense/delete/${id}`,
//         url: to_url,
//         method: 'GET',
//         // data: JSON.stringify(ajaxdata),
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//     // });
//         success: function(data){
//             console.log('Suck! less\n\n');
//             $("#last10msgs").html(data);
//     //     //     console.log(data);
//     //     // //     // console.log(data);
//     //     // //     // $('#mail_list').html(data);
//         }
//     });


// };

// update_ml(); // This will run on page load
// setInterval(function(){
//     update_ml() // this will run after every 5 seconds
// }, 5000);




// function last_10_msgs(){

//     if($("#last_10_msgs").length){


//     var to_url = $("#last_10_msgs").attr('data-to-url');
//     console.log(to_url);
//     $.ajax({
//         url: to_url,
//         method: 'POST',
//         // data: JSON.stringify(ajaxdata),
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success: function(data){
//             console.log('Suck! less\n\n');
//             $("#last_10_msgs").html(data);
//         }
//     });


//     }else{
//     console.log("last_10_msgs does not exists");
//     // var gif_data = '<img src="C:\SDP\postmail\media_pm\resident_media\loading.gif" alt="animated" />';
//     // print(gif_data)
//     // $("#last_10_msgs").html(gif_data);
//     // r'C:\SDP\postmail\media_pm\resident_media\loading_gif'
//     }

// }

// // last_10_msgs(); // This will run on page load
// setInterval(function(){
//     last_10_msgs() // this will run after every 5 seconds
// }, 2000);

