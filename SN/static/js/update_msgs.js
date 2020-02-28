// # update one chat msgs // or update all chats simultaniuosly
function update_msgs(){
    // var url = $(msg).attr('data-to-url'); // create url with appropriate slug of chat
    // var slug = $(chat).attr('data-slug');
    // var ajaxdata = {
    //     slug: slug
    // };
    var url = $('#update_msgs_url').attr('data-url'); //$(location).attr('href');
    $.ajax({
        url: url,
        // data: JSON.stringify(ajaxdata),
        // dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
        success: function(json_rendered_sub_page){
            // or error can be some here
            // console.log('No error to update_msgs html');
            var sub_page = json_rendered_sub_page['data'];
            $('.msgs_in_chat').html(sub_page);
            
        }
    });
    return "OK"
};



var update_msgs_delay = 100;

setTimeout(function run() {
    var msg_update_answer = update_msgs();
    if(msg_update_answer == 'error_overload'){ //ошибка запроса из-за перегрузки сервера
        update_msgs_delay *= 2;
    }
    setTimeout(run, update_msgs_delay);
  }, update_msgs_delay);