var bioInput = $("#wmd-input-id_bio");
var not_show_preview_bio  = $("#wmd-preview-id_bio");

function setBio(value){
    var markedContent = marked(value)
    $("#preview-content").html(markedContent)
    $("#preview-content img").each(function(){
        $(this).addClass("img-responsive")
    })
    not_show_preview_bio.remove();
}

setBio(bioInput.val())

bioInput.keyup(function(){
    var newContent = $(this).val()
    setBio(newContent)
})