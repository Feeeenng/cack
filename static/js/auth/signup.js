function sendCaptcha() {
    // 发送邮件验证码
    var email = $('.form input[name="email"]').val();
    if(checkEmailFormat(email)) {
        var data = {
            'email': email
        };
        $.ajax({
            async : false,
            url: '/send_captcha',
            type: "POST",
            data: JSON.stringify(data),
            dataType   : "json",
            success: function(ret){
                if(ret["detail"]) {
                    alert(ret["detail"]);
                } else {
                    alert(ret["detail"]);
                }
            },
            error: function (ret) {
                alert('网络异常');
            }
        });
    }
}