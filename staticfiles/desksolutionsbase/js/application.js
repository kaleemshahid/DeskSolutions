$(document).ready(function(){

    $('.modal_open_btn').on('click', function () {
        console.log("modal open btn")
        $('.application-upload').trigger('reset');
        // $('#app_form_id')[0].reset();
        $(".application_form_error").hide()
    })
    // $('#btnClose').on('click', function () {
    //     alert("btn close")
    //     $('#app_form_id').trigger('reset');
    // })
    // $('#modal').on('hidden.bs.modal', function(){
    //     console.log("application upload")
    //     $('.application-upload').trigger('reset');
    // })

    $(".success-application").hide()
    $('.application-upload').submit(function (e) {
        e.preventDefault()
        var formdata = new FormData(this)
        // alert("Asdankaknds")
        $.ajax({
            type:"POST",
            url: "",
            // data: $(this).serialize(),
            data: formdata,
            contentType: false,
            processData: false,

            success: (response) => {
                // var form_msg = response
                var form_msg = typeof(response)
                console.log(response)
                console.log(form_msg)
                if (typeof(response) == "object") {
                    // console.log("response me hu")
                    for (var i in response) {
                        // console.log("response ki loop")
                        // if (response[i]>0){
                        //     console.log("i > 0")
                        //     $('.application-upload').parent().html("<p class='lead'>Application submitted successfully! The company will contact you upon qualification")
                        // }
                        // else{
                            // console.log(response[i])
                            // console.log('#id_' + i)
                        //     console.log("nothing")
                        // }
                        
                        var id = '#form-' + i + '-error'
                        console.log(i)
                        console.log(response[i])
                        console.log(id)
                        $(".application_form_error").show()
                        $(id).text(response[i])
                        // $(document).ajaxStop(function() {
                        //     alert("adjasdnk")
                        
                        setTimeout(function() {
                            $(".application_form_error").fadeOut('fast');
                        }, 7000)
                        // });
                        // var id = '#id_' + i
                        // $(id).parent().append(form_msg[i])
                        
                        // console.log(i)
                        // var error_message = "<p style='color: red'>" + response[i] + "</p>"
                        // var id = '#id_' + i
                        // $(id).parent('p').append(response[i])
                    }
 
                } else {
                    console.log("response ni mila")
                    // $('.application-upload').parent().html("<p class=''>Application submitted successfully! The company will contact you upon qualification")
                    // $("#submit-application-btn").hide()
                    $(".modal").modal('hide')
                    // $('#app_form_id').trigger('reset')
                    $('.modal').trigger('reset')
                    $("#success-application").show()
                    $(".application_form_error").hide()
                    setTimeout(function() {
                        $('#success-application').fadeOut('fast');
                    }, 7000)
                    
                }

                
                
            },
            error: function (response) {
                console.log(response)
                // for (var a in response){
                // $('.app_form_error').text(response.responseJSON)
                // }
            }
        })
    })

    // $('[data-role=upButton]').click(function(){
    //     var post_id = $(this).attr('job_id');
    //     var app_id = $("[data-role=application]").attr('app_id');
    //     // post_id.modal()
    //   });
    

})