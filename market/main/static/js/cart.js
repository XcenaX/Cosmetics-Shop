function delete_product(product_id, products_count, csrf_token) {
    $.ajax({
        type: "POST",
        url: "/delete_product_from_bag",
        async: true,
        data: {
            "purchased_product_id": product_id,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            let bag_count = document.getElementById("bag_count").innerHTML;
            document.getElementById("bag_count").innerHTML = (parseInt(bag_count) - products_count).toString();
            document.getElementById("total-price").innerHTML = result['sum_of_products'];
            alert(result['sum_of_products']);
            //alert("product deleted");
        }
    });
}

function add(product_id, product_price, csrf_token) {
    let count = parseInt(document.getElementById("count" + product_id + ".2").innerHTML)

    $.ajax({
        type: "POST",
        url: "/add_product_to_bag",
        async: true,
        data: {
            "count": 1,
            "product_id": product_id,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            document.getElementById("count" + product_id + ".2").innerHTML = (count + 1).toString();
            let bag_count = document.getElementById("bag_count").innerHTML;
            document.getElementById("bag_count").innerHTML = (parseInt(bag_count) + 1).toString();
            document.getElementById("total-price").innerHTML = result['sum_of_products']
        }
    });
}

function buy(money){
    alert(money);
}