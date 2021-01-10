// The offset() method set or returns the offset coordinates for the selected elements, relative to the document.
(function ($) {

    var navbarScrolled = function () {
        if ($("#navbar").offset().top > 100) {
            $("#navbar").addClass("navbar-scrolled")
            console.log("navbar scroll")
        } else {
            $("#navbar").removeClass("navbar-scrolled")
        }
    }

    navbarScrolled();
    // When the page is crolled, ignite this function
    $(window).scroll(navbarScrolled)

    // For active Scrollspy
    $('body').scrollspy({
        target: '#navbar',
        offset: 75
    })

    // Scroll to top
    $('body').scroll(function () {
        var scrollBtn = $(this).scrollTop();
        console.log('scroll to top')
        if (scrollBtn > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    })

})(jQuery);

