var titleInput = $("#id_title");
var not_show_preview_content  = $("#wmd-preview-id_content");

function setTitle(value) {

    $("#preview-title").text(value);
    not_show_preview_content.remove();

}
setTitle(titleInput.val())

titleInput.keyup(function(){
    var newTitle = $(this).val()
    setTitle(newTitle)
})

///////
var contentInput = $("#wmd-input-id_content");

function setContent(value){
    var markedContent = marked(value)
    $("#preview-content").html(markedContent)
    $("#preview-content img").each(function(){
        $(this).addClass("img-responsive")
    })
}

setContent(contentInput.val())

contentInput.keyup(function(){
    var newContent = $(this).val()
    setContent(newContent)
})


