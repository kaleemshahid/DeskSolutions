$(document).ready(function(){
    $("#signup-form").submit(function(e){
        e.preventDefault()

        var formdata = new FormData(this)
        $.ajax({
            type: "POST",
            url: "",
            data: formdata,
            contentType: false,
            processData: false,
            success: (response) => {
                var form_msg = response['register_form']

                if (form_msg) {
                    console.log("Form has errors")
                    for (var i in form_msg) {
                        
                        var error_id = '#error-' + i
                        var id = 'id_' + i
                        console.log(error_id)
                        $(error_id).text(form_msg[i])
                        $(id).addClass('has_error')
                        // $("#form_errors").text(error_message)
                        console.log(form_msg[i])
                        console.log(i)
                    }
                }
                else {
                    console.log("Form submitted")
                    $("#organizationformlink").removeClass('active active_tab1')
                    $("#organizationformlink").removeAttr('href data-toggle')
                    $("#orgtab").removeClass('active')
                    $("#organizationformlink").addClass('inactive_tab1')
                    $("#userformlink").removeClass('inactive_tab1')
                    $("#userformlink").addClass('active active_tab1')
                    $("#userformlink").attr('href', "#usertab")
                    $("#userformlink").attr('data-toggle', "tab")
                    $("#usertab").addClass("active in")
                    // window.location.href = 'profile';
                }
            }
        })
    })

    $("#register-form").submit(function (e){
        alert("Asdasdddddd")
        e.preventDefault()
        $.ajax({
            type: "POST",
            url: "",
            data: $(this).serialize(),
            success: (response) => {
                var form_msg = response['user_form']

                if (form_msg) {
                    console.log("User Form has errors")
                    for (var i in form_msg) {
                        var error_id = '#error-' + i
                        var id = 'id_' + i
                        console.log(error_id)
                        $(error_id).text(form_msg[i])
                        $(id).addClass('has_error')
                        // $("#form_errors").text(error_message)
                        console.log(form_msg[i])
                        console.log(i)
                    }
                }
                else {
                    console.log("success")
                    window.location.href = '../../admin/login';
                }
            }
        })
    })

    $("#lookup_form").submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: "POST",
            url: "",
            data: $(this).serialize(),
            success: (response) => {

                var lookup_not_exist = response['lookup_not_exist']
                var lookup_empty = response['lookup_form']
                var admin_exist = response['admin_exist']
                if (lookup_not_exist){
                    console.log(lookup_not_exist)
                }
                else if(lookup_empty){
                    console.log(lookup_empty)
                }
                else if(admin_exist){
                    console.log(admin_exist)
                }
                else{
                    $("#organizationformlink").removeClass('active active_tab1')
                    $("#organizationformlink").removeAttr('href data-toggle')
                    $("#orgtab").removeClass('active in')
                    $("#organizationformlink").addClass('inactive_tab1')
                    $("#userformlink").removeClass('inactive_tab1')
                    $("#userformlink").addClass('active active_tab1')
                    $("#userformlink").attr('href', "#usertab")
                    $("#userformlink").attr('data-toggle', "tab")
                    $("#usertab").addClass("active in")
                }
            }
        })
    })
})