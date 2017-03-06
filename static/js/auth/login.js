function getLoginCaptcha() {
    var url = '/get_login_captcha';
    $.ajax({
        async : false,
        url: url,
        type: 'GET',
        dataType   : "json",
        success: function(ret){
            if(ret["success"]) {
                $('#login_captcha').attr('src', ret['data']);
            }
        },
        error: function (ret) {
            alert('网络异常');
        }
    });
}

$(document).ready(function () {
    getLoginCaptcha();
});

function submitLoginForm() {
    // 提交登录表单
    var data = $('#login').serialize();
    $.ajax({
        async : false,
        url: '/login',
        type: "POST",
        data: data,
        dataType   : "json",
        success: function(ret){
            if(!ret["success"]) {
                errorPrompt(ret["filed_name"], ret["error"]);
                getLoginCaptcha();
            } else {
                location.href = ret["url"];
            }
        },
        error: function (ret) {
            alert('网络异常');
        }
    });
}

function submitFindPasswordForm(obj) {
    // 提交找回密码表单
    var data = $('#find_pass_word_form').serialize();
    $.ajax({
        async : false,
        url: '/forget_password',
        type: "POST",
        data: data,
        dataType   : "json",
        success: function(ret){
            if(!ret["success"]) {
                errorPrompt(ret["filed_name"], ret["error"]);
            } else {
                lockButton(obj, 'Send email');
                showSentEmailMessage()
            }
        },
        error: function (ret) {
            alert('网络异常');
        }
    });
}

function showFindPasswordBox() {
    $('#find_pass_word_form input[name="find_password_email"]').val('');
    $('#find_pass_word').transition('drop');
}

function showSentEmailMessage() {
    // 展示发送邮件后的消息
    var x = function () {
        $('#loading_message').transition('swing down', '2s');
    };
    $('#loading_message').transition('swing down', '2s', function(){
        setTimeout(x, 5000)
    })
}
