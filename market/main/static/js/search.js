$( document ).ready(function() {
    function selectCkick(){
        this.size=1; 
        this.blur();
        button = $("#search_button2");
        button.click();
    }
    
    $("#select-price").change(selectCkick);
    $("#select-brand").change(selectCkick);
    $("#select-category").change(selectCkick);
});
