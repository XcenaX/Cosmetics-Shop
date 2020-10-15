function buy(product_id, is_one_product, count=1){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    if(!is_one_product){
        if($("#count").length > 0){
            count = parseInt($("#count").text());
        }
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

