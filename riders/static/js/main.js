// This is the function that hides the car animation.
setTimeout(function () {
    $('.animation').fadeOut('fast');
}, 3000);


// <!-- #tagline transition -->
$(document).ready(function () {
    setTimeout(function () {
        $('#main').removeClass('is-loading');
    }, 100)
});

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

//Side nav toggle
$('.button-collapse').sideNav();

///Materialize Timepicker
var el = document.querySelector('.timepicker');
M.Timepicker.init(el, { 
    twelveHour: false,
    showClearBtn: true,
 });

///Materalize dropdown options
$(document).ready(function () {
    $('select').material_select();
});


///Disable dropdown from having the same options selected on search page
function preventDupes(select, index) {
    var options = select.options,
        len = options.length;
    while (len--) {
        options[len].disabled = false;
    }
    select.options[index].disabled = true;
    $('select').material_select();
}

var select1 = document.getElementById('select1');
var select2 = document.getElementById('select2');

select1.onchange = function () {
    preventDupes.call(this, select2, this.selectedIndex);
};

select2.onchange = function () {
    preventDupes.call(this, select1, this.selectedIndex);
};