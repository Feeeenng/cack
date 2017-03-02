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
    // 提交表单
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

