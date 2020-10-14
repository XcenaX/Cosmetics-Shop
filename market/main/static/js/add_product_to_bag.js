function buy(product_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    try{
        count = parseInt($("#count").text());
    } catch{
        count = 1;
    }
    console.log(count);
    $.ajax({
        type: "POST",
        url: "/add_product_to_bag", 
        async: true,
        
        data: {
            "product_id": product_id,
            "csrfmiddlewaretoken": csrf,
            "count": count,
        },
        success: function(result){
            bag_text = $("#bag_count");
            var old_count = parseInt(bag_text.text());
            bag_text.text(old_count+count);
            alertify.success("Товар добавлен в корзину!",2)
        }
    });
}

