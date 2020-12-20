$(document).ready(function (){
    $("#contact-success-msg").hide()
    $(".error-span").hide()
    $("#contact_form_id").submit(function (e){
        e.preventDefault()

        $.ajax({
            type : "POST",
            url : "",
            data : $(this).serialize(),
            success : (response) => {
                console.log(response)
                // var contact_response = response
                // if (response){
                //     for (i in response){
                //         console.log(i)
                //         var error_id = "#error-" + i
                //         $(error_id).text(response[i])
                //         setTimeout(function() {
                //             $(".error-span").fadeOut('fast');
                //         }, 4000)
                //     }
                // }
                // else{
                    console.log("success")
                    $('#contact_form_id').trigger('reset')
                    $("#contact-success-msg").show()
                    setTimeout(function() {
                        $("#contact-success-msg").fadeOut('fast');
                    }, 4000)
                // }
            },
            error : (response) => {
                var contact_response = response.responseJSON
                for (i in contact_response){
                    console.log(contact_response[i])
                    
                    var error_id = "#error-" + i
                    $(error_id).text(contact_response[i])
                    $(".error-span").show()
                    setTimeout(function() {
                        $(".error-span").fadeOut('fast');
                    }, 4000)
                }
            }
        })
    })
})