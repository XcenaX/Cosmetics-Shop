$( document ).ready(function() {
    $("#close-menu").click(function(){
        $("#open-menu").css("transform", "rotate(-90deg)");
        $("#close-menu").css("transform", "rotate(-90deg)");
        $("#mobile-header-menu").height("0%");
        $("html").css("overflow", "inherit")
        $("body").css("overflow", "scroll")
        setTimeout(function(){$("#mobile-header-menu").hide();}, 180)
        
    });

    $("#open-menu").click(function(){
        $("#open-menu").css("transform", "rotate(0deg)");
        $("html").css("overflow", "hidden")
        $("body").css("overflow", "hidden")
        $("#mobile-header-menu").css("display", "block");
        $("#mobile-header-menu").height("100%");
        $("#close-menu").css("transform", "rotate(0deg)");
        
    });

    $("#search-icon").mouseenter(function(){
        $("#search").css("opacity", "1");
    });
    $("#search-icon").mouseleave(function(){
        $("#search").css("opacity", "0");
    });
});

// for(var i = 100; i >= 0; i-=2){
//     $("#mobile-header-menu").height(i + "%");
    
// }
// for(var i = 0; i <= 100; i+=2){
//     var width = i + "%";

// }