$(document).ready(function(){
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
            success: function(response){
                console.log("success")
                // console.log(response)
                for (var i in response) {
                    console.log(response[i])
                    var error_message = "<p style='color: red'>" + response[i] + "</p>"
                    var id = '#id_' + i
                    $(id).parent('p').append(response[i])
                    
                }

            }
        })
    })

    $('[data-role=upButton]').click(function(){
        var post_id = $(this).attr('job_id');
        var app_id = $("[data-role=application]").attr('app_id');
        // post_id.modal()
      });

})