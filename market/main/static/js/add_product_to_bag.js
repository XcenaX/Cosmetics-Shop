function buy(product_id, url, csrf_token){
    $.ajax({
        type: "POST",
        url: "/add_product_to_bag", 
        async: true,
        
        data: {
            "product_id": product_id,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            bag_text = $("#bag_count");
            var count = parseInt(bag_text.text());
            bag_text.text(++count);
            alertify.success("Товар добавлен в корзину!",2)
        }
    });
}

