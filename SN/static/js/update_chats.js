
// # update one chat msgs // or update all chats simultaniuosly
function update_chats(){
    // var url = $(msg).attr('data-to-url'); // create url with appropriate slug of chat
    // var slug = $(chat).attr('data-slug');
    // var ajaxdata = {
    //     slug: slug
    // };
    var url = $('#update_chats_url').attr('data-url'); //$(location).attr('href');
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
            $('.main_list_chats').html(sub_page);
            
        }
    });
    return "OK"
};




function setOnInterval(){

    var update_msgs_delay = 100;

    setTimeout(function run() {
        var msg_update_answer = update_chats();
        if(msg_update_answer == 'error_overload'){ //ошибка запроса из-за перегрузки сервера
            update_msgs_delay *= 2;
        }
        setTimeout(run, update_msgs_delay);
    }, update_msgs_delay);
    
};



$(document).ready(function($) {
    console.log( "ready!" );
    var data_switch = $('#manage_timeouts').attr('data-to-manage');
    console.log(data_switch);
    if(data_switch == 'On'){
        setOnInterval();
    }
});