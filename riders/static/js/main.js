// This is the function that hides the car animation.
setTimeout(function () {
    $('.animation').fadeOut('fast');
}, 3000);


// Carousel on landing page
$(document).ready(function () {
    $('.carousel').carousel(
        {
            dist: 0,
            padding: 0,
            fullWidth: true,
            indicators: true,
            duration: 300,
        }
    );
});


