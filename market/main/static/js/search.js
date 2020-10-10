$( document ).ready(function() {
    $("#select-price").change(function(){
        button = $("#search_button2");
        button.click();
        console.log("test")
    });
    
    $("#select-brand").change(function(){
        button = $("#search_button2");
        button.click();
    });
});
