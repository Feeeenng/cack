$.fn.form.settings.rules.checkUsernameFormat = function(username){
    var flag = false;
    var data = {
        'username': username
    };
    $.ajax({
        async : false,
        url: '/auth/username_regex',
        type: "POST",
        data: JSON.stringify(data),
        dataType   : "json",
        success: function(ret){
            flag = ret["detail"];
        }
    });
    return flag;
};

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

$('.ui.checkbox').checkbox();

$('#login-form').form({
    username: {
        identifier: 'username',
        rules: [
            {
                type: 'empty',
                prompt: '请输入用户名'
            },
            {
                type: 'checkUsernameFormat',
                prompt: '用户名必须是8-20位字母和数字的组合, 第一位必须为字母'
            }
        ]
    },
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
    }
}, {
    on: 'submit',
    inline: true
});

$('#login').click(function () {
    $('#login-form').submit();
});