

$(document).ready(function(){
  $(".slider .owl-carousel").owlCarousel({
  	nav:true,
  	loop:true,
  	items:1,
  	dots:false
  });
    $(".featured-slider .owl-carousel").owlCarousel({
  	nav:true,
  	loop:true,
  	items:4,
  	dots:false,
  	margin:10,
  	responsive:{
        0:{
            items:1
        },
        500:{
            items:2
        },
        800:{
            items:3
        },
        1000:{
            items:4
        }
    }
  });
});