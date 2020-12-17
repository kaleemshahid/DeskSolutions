$(document).ready(function(){

    // $('#modal_open_btn').on('click', function () {
    //     // $('#app_form_id').trigger('reset');
    //     $('#app_form_id')[0].reset();
    // })
    // $('#btnClose').on('click', function () {
    //     alert("btn close")
    //     $('#app_form_id').trigger('reset');
    // })
    $('#modal').on('hidden.bs.modal', function(){
        $('#app_form_id').trigger('reset');
    })
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
                        if (i == ""){
                        // console.log($(".form-field").children(id).children())
                        // $(id).hide()
                        console.log(i)
                            $(id).text(response[i])
                        }
                        else if(i == ""){
                            console.log("asdsad")
                        }
                        else{
                            console.log("id no")
                            $(id).text("")
                        }
                        // var id = '#id_' + i
                        // $(id).parent().append(form_msg[i])
                        
                        // console.log(i)
                        // var error_message = "<p style='color: red'>" + response[i] + "</p>"
                        // var id = '#id_' + i
                        // $(id).parent('p').append(response[i])
                    }
                } else {
                    console.log("response ni mila")
                    $('.application-upload').parent().html("<p class=''>Application submitted successfully! The company will contact you upon qualification")
                    $("#submit-application-btn").hide()
                    $('#app_form_id').trigger('reset');

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

    $('[data-role=upButton]').click(function(){
        var post_id = $(this).attr('job_id');
        var app_id = $("[data-role=application]").attr('app_id');
        // post_id.modal()
      });

})