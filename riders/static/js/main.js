// This is the function that hides the car animation.
// In deployment, we'll likely want the time to be between 3000 and 60000 milleseconds
setTimeout(function () {
    $('.animation').fadeOut('fast');
}, 1000);


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

