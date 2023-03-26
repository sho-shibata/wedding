
$(function(){
    
    let topImageHeight = $(window).height();
    let topImageWidth = $(window).width();
    if(topImageWidth <= 480){
        $('.top-image-container').css('height', topImageHeight + 'px');
        $('.top-image').css('height', topImageHeight + 'px');
        $('.top-image').css('height', topImageHeight + 'px');
    }else{
        $('.top-image-container').css('width', '50vw');
        $('.top-image-container').css('height', '50vw');
        $('.top-image-container').css('margin', '0 auto');
    }
    $('body').css('max-width', topImageWidth);

});

