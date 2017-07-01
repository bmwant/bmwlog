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

    var currentLanguage = $("input[name=language]").val();
    $(".lang-icon[data-lang="+currentLanguage+"]").addClass("radio-selected");
    $(".lang-icon").click(function() {
        $(".lang-icon").removeClass("radio-selected");
        $(this).addClass("radio-selected");
        $("input[name=language]").val($(this).data("lang"));
    });
    
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
    
    var editorInstance = CKEDITOR.replace('article-text');

    Dropzone.options.imageDropzone = {
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 3, // MB
        dictDefaultMessage: "Upload image",
        success: function(file, status) {
            var path = $("<input/>", {
                type: 'text',
                value: status,
                readonly: 1
            });
            $(".dz-success-mark").append(path);
            console.log(status);
        }
    };
});

window.onbeforeunload = function () {
    var editorInstance = CKEDITOR.instances["article-text"];
    var isDirty = editorInstance.getData() !== "";
    if (isDirty) {
        return "There are unsaved data.";
    }
    return undefined;
};
