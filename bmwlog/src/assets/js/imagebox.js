import $ from 'jquery'

export function imageBox() {
// ACTIVITY INDICATOR

var activityIndicatorOn = function () {
      $('<div id="imagelightbox-loading"><div></div></div>').appendTo('body');
    },
    activityIndicatorOff = function () {
      $('#imagelightbox-loading').remove();
    },


// OVERLAY
    overlayOn = function () {
      $('<div id="imagelightbox-overlay"></div>').appendTo('body');
    },
    overlayOff = function () {
      $('#imagelightbox-overlay').remove();
    },


// CLOSE BUTTON
    closeButtonOn = function (instance) {
        $('<button type="button" id="imagelightbox-close" title="Close"></button>').appendTo('body').on('click touchend', function () {
            $(this).remove();
            instance.quitImageLightbox();
            return false;
        });
    },
    closeButtonOff = function () {
        $('#imagelightbox-close').remove();
    },


// CAPTION
    captionOn = function () {
        var description = $('a[href="' + $('#imagelightbox').attr('src') + '"] img').attr('alt');
        if (description.length > 0)
            $('<div id="imagelightbox-caption">' + description + '</div>').appendTo('body');
    },
    captionOff = function () {
        $('#imagelightbox-caption').remove();
    }

    var selectorF = '.gallery a';
    var instanceF = $(selectorF).imageLightbox({
        onStart:		function() { overlayOn(); closeButtonOn( instanceF ); },
        onEnd:			function() { overlayOff(); captionOff(); closeButtonOff(); activityIndicatorOff(); },
        onLoadStart: 	function() { captionOff(); activityIndicatorOn(); },
        onLoadEnd:	 	function() { captionOn(); activityIndicatorOff(); }
    });
}
