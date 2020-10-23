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

            let pcProduct = document.getElementById("product" + product_id + ".1");
            let mobileProduct = document.getElementById("product" + product_id + ".2");
            pcProduct.parentNode.removeChild(pcProduct);
            mobileProduct.parentNode.removeChild(mobileProduct);
        }
    });
}

function delete_one_product(product_id, csrf_token){
    let count = parseInt(document.getElementById("count" + product_id + ".2").innerHTML)
    if(count > 1){
        $.ajax({
            type: "POST",
            url: "/delete_one_product_from_bag",
            async: true,
            data: {
                "purchased_product_id": product_id,
                "csrfmiddlewaretoken": csrf_token,
            },
            success: function(result){
                let bag_count = document.getElementById("bag_count").innerHTML;
                document.getElementById("bag_count").innerHTML = (parseInt(bag_count) - 1).toString();
                document.getElementById("total-price").innerHTML = result['sum_of_products'];

                document.getElementById("count" + product_id + ".2").innerHTML = (count - 1).toString();
                document.getElementById("count" + product_id + ".1").innerHTML = (count - 1).toString();
            }
        });
    }
}

function add(product_id, product_price, csrf_token) {
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
            var count = result["count"];
            var all_count = result["all_count"];
            document.getElementById("count" + product_id + ".2").innerHTML = (count).toString();
            document.getElementById("count" + product_id + ".1").innerHTML = (count).toString();
            let bag_count = document.getElementById("bag_count").innerHTML;
            document.getElementById("bag_count").innerHTML = (all_count).toString();
            document.getElementById("total-price").innerHTML = result['sum_of_products']
        }
    });
}

function delete_share(share_id, shares_count, csrf_token) {
    $.ajax({
        type: "POST",
        url: "/delete_share_from_bag",
        async: true,
        data: {
            "purchased_share_id": share_id,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            let bag_count = document.getElementById("bag_count").innerHTML;
            document.getElementById("bag_count").innerHTML = (parseInt(bag_count) - shares_count).toString();
            document.getElementById("total-price").innerHTML = result['sum_of_products'];

            let pcProduct = document.getElementById("share" + share_id + ".1");
            let mobileProduct = document.getElementById("share" + share_id + ".2");
            pcProduct.parentNode.removeChild(pcProduct);
            mobileProduct.parentNode.removeChild(mobileProduct);
        }
    });
}

function delete_one_share(share_id, csrf_token){
    let count = parseInt(document.getElementById("share_count" + share_id + ".2").innerHTML)
    if(count > 1){
        $.ajax({
            type: "POST",
            url: "/delete_one_share_from_bag",
            async: true,
            data: {
                "purchased_share_id": share_id,
                "csrfmiddlewaretoken": csrf_token,
            },
            success: function(result){
                let bag_count = document.getElementById("bag_count").innerHTML;
                document.getElementById("bag_count").innerHTML = (parseInt(bag_count) - 1).toString();
                document.getElementById("total-price").innerHTML = result['sum_of_products'];

                document.getElementById("share_count" + share_id + ".2").innerHTML = (count - 1).toString();
                document.getElementById("share_count" + share_id + ".1").innerHTML = (count - 1).toString();
            }
        });
    }
}

function add_share(share_id, product_price, csrf_token) {
    $.ajax({
        type: "POST",
        url: "/add_share_to_bag",
        async: true,
        data: {
            "count": 1,
            "share_id": share_id,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            var count = result["count"];
            var all_count = result["all_count"];
            console.log("share_count" + share_id + ".2");
            document.getElementById("share_count" + share_id + ".2").innerHTML = (count).toString();
            document.getElementById("share_count" + share_id + ".1").innerHTML = (count).toString();
            let bag_count = document.getElementById("bag_count").innerHTML;
            document.getElementById("bag_count").innerHTML = (all_count).toString();
            document.getElementById("total-price").innerHTML = result['sum_of_products']
        }
    });
}

function buy(money){
    alert(money);
}