$(document).ready(function () {
    $(".form_error").hide()
    const form = document.getElementById('signup-form')
    var title = document.getElementById('id_title')

    $('#signup-form').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: "",
            data: $(form).serialize(),
            success: function (response) {
                var form_msg = response['register_form']
                if (form_msg) {
                    console.log("Form has errors")
                    for (var i in form_msg) {
                        var error_message = "<p style='color: red'>" + form_msg[i] + "</p>"
                        var id = '#id_' + i
                        $(id).parent('p').append(form_msg[i])
                        $(id).addClass('ss');
                        $("#form_error").show(form_msg[i])

                        // $("#form_errors").text(error_message)
                        console.log(form_msg[i])
                        console.log(i)
                    }
                }
                else {
                    console.log("Form submitted")
                    window.location.href = 'profile';
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    })
})