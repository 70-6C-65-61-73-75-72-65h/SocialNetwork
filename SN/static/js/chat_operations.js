

function delete_chat(chat){
    var url = $(chat).attr('data-to-url');
    var slug = $(chat).attr('data-slug');
    if (typeof $(chat).attr('data-detail') == 'undefined'){
        console.log($(chat));
        var $chat = $(chat);
        $chat.parent().parent().parent().parent().remove();
    };
    var ajaxdata = {
        slug: slug
    };
    $.ajax({
        url: url,
        data: JSON.stringify(ajaxdata),
        dataType: 'json',
        method: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });
};


// function create_custom_chat(chat){
//     if($('#create_custom_chat').css({'visibility': 'hidden'})){
//         $('#create_custom_chat').css({'visibility': 'visible'});
//     }
//     else{
//         $('#create_custom_chat').css({'visibility': 'hidden'});
//     };
    
//     // var url = $(chat).attr('data-to-url');
//     // var ajaxdata = {};
//     // $.ajax({
//     //     url: url,
//     //     data: JSON.stringify(ajaxdata),
//     //     dataType: 'json',
//     //     method: 'POST',
//     //     beforeSend: function (xhr) {
//     //         xhr.setRequestHeader('X-CSRFToken', csrf_token)
//     //     },
//     //     success: function(answer){
//     //         console.log(answer);
//     //         $('.mail_answer').html(answer);
//     //     }
//     // });
// };


// 1 step ( can be only render answer to that ajax)
function create_msg(msg){
    var url = $(msg).attr('data-to-url'); // create url with appropriate slug of chat
    // var slug = $(chat).attr('data-slug');
    // var ajaxdata = {
    //     slug: slug
    // };
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
            console.log('No error to create_msg popup html')
            var sub_page = json_rendered_sub_page['data'];
            $('.create_msg').html(sub_page);
            
        }
    });
};

// 2 step
function send_msg(msg){
    var url = $(msg).attr('data-to-url'); // create url with appropriate slug of chat
    var form = $("#create_msg_form").serialize();
    // var slug = $(chat).attr('data-slug');
    // var ajaxdata = {
    //     form: new FormData($('#create_msg_form')[0])
    // };
    var ajaxdata = {
        form: new FormData($('#create_msg_form')[0])
    };
    $.ajax({
        url: url,
        data: JSON.stringify(ajaxdata), //form,
        // data: JSON.stringify(ajaxdata),
        dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
        success: function(json_rendered_sub_page){
            
            if(json_rendered_sub_page['data'] == "0"){
                console.log('!!!!!!!!!!!!!!!!data false pisos');
            }
            else if(json_rendered_sub_page['data'] == "1"){
                console.log('successfully created msg!!!!!!!!!!!');
                var suspend_html = `<p><a data-to-url="`+url+`" onclick="create_msg(this)" class="btn btn-primary" role="button">Create Message</a></p>`;
                $('.create_msg').html(suspend_html);
            }
            else{
                var sub_page = json_rendered_sub_page['data'];
                
                $('.create_msg').html(sub_page);
            };
            
        }
    });
};



function create_custom_chat(chat){
    var url = $(chat).attr('data-to-url');
    var ajaxdata = {};
    $.ajax({
        url: url,
        data: JSON.stringify(ajaxdata),
        dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
        success: function(json_rendered_sub_page){
            
            var sub_page = json_rendered_sub_page['data'];
            $('.create_custom_chat').html(sub_page);
            
        }
    });
};

function for_form_ccc(chat){
    var url = $(chat).attr('data-to-url'); // create url with appropriate slug of chat
    var form = $("#create_custom_chat_form").serialize();
    // var slug = $(chat).attr('data-slug');
    // var ajaxdata = {
    //     slug: slug
    // };
    $.ajax({
        url: url,
        data: form,
        // data: JSON.stringify(ajaxdata),
        dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
        success: function(json_rendered_sub_page){
            
            if(json_rendered_sub_page['data'] == "0"){
                console.log('!!!!!!!!!!!!!!!!data false pisos');
            }
            else if(json_rendered_sub_page['data'] == "1"){
                console.log('successfully created msg!!!!!!!!!!!');
                var suspend_html = `<p><a data-to-url='{% url "chats:chat_create" %}' onclick="create_custom_chat(this)" class="btn btn-default" role="button">Create Custom Chat</a></p>`;
                $('.create_custom_chat').html(suspend_html);
            }
            else{
                var sub_page = json_rendered_sub_page['data'];
                
                $('.create_custom_chat').html(sub_page);
            };
            
        }
    });
};



// // # update one chat msgs // or update all chats simultaniuosly
// function update_msgs(){
//     // var url = $(msg).attr('data-to-url'); // create url with appropriate slug of chat
//     // var slug = $(chat).attr('data-slug');
//     // var ajaxdata = {
//     //     slug: slug
//     // };
//     var url = 'chats:update_msgs_and_chats';
//     $.ajax({
//         url: url,
//         // data: JSON.stringify(ajaxdata),
//         // dataType: 'json',
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success: function(json_rendered_sub_page){
//             // or error can be some here
//             console.log('No error to create_msg popup html')
//             var sub_page = json_rendered_sub_page['data'];
//             $('.create_msg').html(sub_page);
            
//         }
//     });
// };



// var update_msgs_delay = 200;

// setTimeout(function run() {
//     var msg_update_answer = update_msgs();
//     if(msg_update_answer == 'error_overload'){ //ошибка запроса из-за перегрузки сервера
//         update_msgs_delay *= 2;
//     }
//     setTimeout(run, update_msgs_delay);
//   }, update_msgs_delay);




// $("p").css({"background-color": "yellow", "font-size": "200%"});
// .hide();
// .show();
// function create_chat(chat){
//     var url = $(chat).attr('data-to-url');
//     var ajaxdata = {};
//     $.ajax({
//         url: url,
//         data: JSON.stringify(ajaxdata),
//         dataType: 'json',
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         }
//     });
// }
// // pop
// function mail_answer(mail){
//     var url = $(mail).attr('data-to-url');

//     var mail_thread_id = $(mail).attr('data-mailthread-id');
//     var operation = $(mail).attr('data-operation');


//     var ajaxdata = {
//         mail_thread_id: mail_thread_id,
//         operation: operation
//     };


//     console.log(url);
//     console.log(mail_id);
//     console.log(operation);

//     $.ajax({
//         url: url,
//         data: JSON.stringify(ajaxdata),
//         dataType: 'json',
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success: function(answer){
//             // console.log(answer);
//             $('.mail_answer').html(answer);
//         }
//     });

// };
// // send
// $("#submit").onclick(function(){
//     var url = $(this).attr('data-to-url');
//     console.log(url);

//     $.ajax({
//         url: url,
//         data: JSON.stringify(ajaxdata),
//         dataType: 'json',
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success: function(answer){
//             // console.log(answer);
//             var recursive_str = `<p><a data-to-url="{% url 'mails:answer' operation='pop' to_mail_id=instance.id %}" onclick="mail_answer(this)" class="btn btn-primary" role="button">Answer</a></p>`;
//             $('.mail_answer_append').html(recursive_str);
//         }
//     });



// m_form
// $(msg).serialize(),
// Cool

// send msg to chat ( only for msg-form id)
// $('#msg-form').on('submit', function(msg){
//     $.ajax({
//         url: $(msg).attr('data-to-url'),
//         data: $(this).serialize(),
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success:function(answer){

//             document.getElementById("error-msg").html();

//             if (answer['created'] == true){
//                 document.getElementById("msg-form").reset();
//             }
//             else{
//                 document.getElementById("msg-form").reset();
//                 document.getElementById("error-msg").html('<h4><i><b>Заполните поле контента сообщения для отправки</b></i></h4><hr><h5>Или другая ошибка</h5>');
//             };
            
//         },
//         error : function(xhr,errmsg,err) {
//         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//     }
//     });
// });



// // send msg to chat ( only for msg-form id)
// $('#custom-chat-creation-form').on('submit', function(msg){
//     $.ajax({
//         url: $(msg).attr('data-to-url'),
//         data: $(this).serialize(),
//         method: 'POST',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         },
//         success:function(answer){
//             console.log('suck sess');
//         },
//         error : function(xhr,errmsg,err) {
//         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//     }
//     });
// });
























// function update_like(post){ // like like_thread
//     var to_url = $(post).attr('data-to-url'); //  TODO!!!
//     // var slug = $(post).attr('data-slug');
//     var from_url = $(post).attr('data-from-url');
//     // var user = $(post).attr('data-user');
//     // if (typeof $(post).attr('data-detail') == 'undefined'){
//     //     console.log($(post));
//     //     var $post = $(post);
//     //     $post.parent().parent().parent().parent().parent().remove();
//     // };
//     var ajaxdata = {
//         // slug: slug,
//         from_url: from_url,
//         // user: user,
//     };
//     $.ajax({
//         url: to_url,
//         data: JSON.stringify(ajaxdata),
//         dataType: 'json',
//         method: 'PUT',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         }
//     });
// };

// function like_thread(post){ // like update_like
//     var to_url = $(post).attr('data-to-url');
//     var slug = $(post).attr('data-slug');
//     var from_url = $(post).attr('data-from-url');
//     var user = $(post).attr('data-user');
//     // if (typeof $(post).attr('data-detail') == 'undefined'){
//     //     console.log($(post));
//     //     var $post = $(post);
//     //     $post.parent().parent().parent().parent().parent().remove();
//     // };
//     var ajaxdata = {
//         slug: slug,
//         from_url: from_url,
//         user: user,
//     };
//     $.ajax({
//         url: to_url,
//         data: JSON.stringify(ajaxdata),
//         dataType: 'json',
//         method: 'GET',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', csrf_token)
//         }
//     });
// };

// получить id of essense, class of essence and send post ajax to delete that 
// html had from-url, to-url, data-slug