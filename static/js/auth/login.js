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


$(function () {
    $("#captcha_input").keyup(function () {
        //如果输入非数字，则替换为''，如果输入数字，则在每4位之后添加一个空格分隔
        var v = this.value;
        var r_v = this.value.replace(/[^\d]/g, '');
        if(v!=r_v){
            errorPrompt('captcha', 'Captcha is a number');
        } else {
            blurRemoveErrorPrompt(this);
        }
        this.value = r_v;
    })
});
