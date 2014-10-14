/**
 * Created by Administrator on 06.10.14.
 */
function toDrafts() {
    $("input[name=draft]").val(1);
}

function publish() {
    $("input[name=draft]").val(0);
}

function applyTags() {
    $("input[name=tags]").val(
        $("#tagBox").tagging('getTags').join(";")
    );
}

$(document).ready(function() {

    var tag_options = {
        "no-duplicate": true,
        "no-duplicate-callback": undefined,
        "no-duplicate-text": "Duplicate tags",
        "type-zone-class": "type-zone",
        "tag-box-class": "tagging",
        "forbidden-chars": [",", ".", "_", "?", "!", ":", " "],
        "edit-on-delete": false,
        "no-comma": true,
        "no-enter": true,
        "no-spacebar": false,
        "pre-tags-separator": ";",
        "tag-class": "tag_input",
        "tags-input-name": "tag_input"
    };

    $("#tagBox").tagging(tag_options);

    $("#submitter").click(function(){
        applyTags();
        publish();
        $(this).closest('form').submit();
    });

    $("#drafter").click(function(){
        applyTags();
        toDrafts();
        $(this).closest('form').submit();
    });


    CKEDITOR.replace('article-text');
    CKEDITOR.editorConfig = function(config) {};

    Dropzone.options.imageDropzone = {
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 3, // MB
        dictDefaultMessage: "Завантажити картинку",
        success: function(file, status) {
            console.log(status);
        }
    };
})