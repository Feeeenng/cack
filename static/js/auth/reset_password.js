function submitResetPasswordForm() {
        // 提交找回密码表单
    var data = $('#reset_password').serialize();
    $.ajax({
        async : false,
        url: $('#reset_password').attr('action'),
        type: "POST",
        data: data,
        dataType   : "json",
        success: function(ret){
            if(!ret["success"]) {
                errorPrompt(ret["filed_name"], ret["error"]);
            } else {
                location.href = ret["url"];
            }
        },
        error: function (ret) {
            alert('网络异常');
        }
    });
}