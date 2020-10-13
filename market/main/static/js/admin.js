function remove_parameter(name, csrf_token){
    $.ajax({
        type: "POST",
        url: "/delete_session_parameter", 
        async: true,
        data: {
            "name": name,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function(result){
            
        }
    });
}