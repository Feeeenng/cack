$.fn.form.settings.rules.checkPasswordFormat = function(password){
    var flag = false;
    var data = {
        'password': password
    };
    $.ajax({
        async : false,
        url: '/auth/password_regex',
        type: "POST",
        data: JSON.stringify(data),
        dataType   : "json",
        success: function(ret){
            flag = ret["detail"];
        }
    });
    return flag;
};

$('#find-password-form').form({
    password: {
        identifier: 'password',
        rules: [
            {
                type: 'empty',
                prompt: '请输入密码'
            },
            {
                type: 'checkPasswordFormat',
                prompt: '密码必须是6-20位字母和数字的组合, 第一位必须为大字母'
            }
        ]
    },
    confirm: {
        identifier: 'confirm',
        rules: [
            {
                type: 'empty',
                prompt: '重复密码不能为空'
            },
            {
                type: 'match[password]',
                prompt: '密码不一致'
            }
        ]
    }
}, {
    on: 'submit',
    inline: true,
    onSuccess: submitFindPasswordForm
});

$('#find-password-submit').click(function () {
    $('#find-password-form').submit(function () {
        return false;
    });
});

function submitFindPasswordForm() {
    var data = $('.ui.form input').serializeArray();
    $.ajax({
        async : false,
        url: $('.ui.form').attr('action'),
        type: 'POST',
        data: data,
        dataType   : 'json',
        success: function(ret){
            var success = ret['success'];
            if(success){
                location.href = ret['detail']['url'];
            }else{
                var msg = ret['error'];
                new jBox('Notice', {
                    content: msg,
                    color: 'black',
                    animation: 'slide',
                    position: {
                        x: 100,
                        y: 100
                    }
                });
            }
        },
        error: function () {
            new jBox('Notice', {
                content: msg,
                color: 'red',
                animation: 'slide',
                position: {
                    x: 100,
                    y: 100
                }
            });
        }
    });
}