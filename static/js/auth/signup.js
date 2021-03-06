function sendCaptcha(obj) {
    // 发送邮件验证码
    var email = $('.form input[name="email"]').val();
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
            if(!ret["success"]) {
                errorPrompt("email", ret["error"]);
            } else {
                alert("邮件已发送"); //展示
                lockButton(obj, 'Send captcha');
                showSentEmailMessage();
            }
        },
        error: function (ret) {
            alert('网络异常');
        }
    });
}

function submitForm() {
    // 提交表单
    var data = $('#signup').serialize();
    $.ajax({
        async : false,
        url: '/signup',
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