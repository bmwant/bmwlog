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
  var tagOptions = {
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
    
    $("#tagBox").tagging(tagOptions);
    $('input[name="title"]').focusout(function() {
      $.get('/get_slug', {'title': $(this).val()}, function(data) {
        $('input[name="slug"]').val(data);
      });
    });

    $("#submitter").click(function() {
      applyTags();
      publish();
      window.onbeforeunload = undefined;
      $(this).closest('form').submit();
    });

    $("#drafter").click(function() {
      applyTags();
      toDrafts();
      window.onbeforeunload = undefined;
      $(this).closest('form').submit();
    });

  window.editor = new SimpleMDE({
    element: document.getElementById("article-text")
  });

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

notifyChangesPresent = function () {
  var isDirty = window.editor
    .codemirror.doc.getValue() !== $("#article-text").text();
  if (isDirty) {
    return "There are unsaved changes!";
  }
  return undefined;
};

window.onbeforeunload = notifyChangesPresent;
