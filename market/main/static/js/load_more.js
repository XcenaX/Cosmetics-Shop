$( document ).ready(function () {
    $(".moreBox").slice(0, 3).show();
    if ($(".hide-rate").length != 0) {
        $("#loadMore").show();
    }   
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        var elems = $(".hide-rate").slice(0, 4);
        
        [].forEach.call(elems, function(el) {
            el.classList.remove("hide-rate");
        });

        if ($(".hide-rate").length == 0) {
            $("#loadMore").fadeOut('slow');
        }
    });
});