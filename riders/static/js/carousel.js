// Carousel on landing page works with main.js
function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 10000);
};
autoplay();
