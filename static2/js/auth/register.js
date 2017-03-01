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

$.fn.form.settings.rules.checkEmailFormat = function(email){
    var flag = false;
    var data = {
        'email': email
    };
    $.ajax({
        async : false,
        url: '/auth/email_regex',
        type: "POST",
        data: JSON.stringify(data),
        dataType   : "json",
        success: function(ret){
            flag = ret["detail"];
        }
    });
    return flag;
};

$.fn.form.settings.rules.checkUsername = function(username){
    var flag = false;
    var data = {
        'username': username
    };
    $.ajax({
        async : false,
        url: '/auth/check_username',
        type: "POST",
        data: JSON.stringify(data),
        dataType   : "json",
        success: function(ret){
            flag = ret["detail"];
        }
    });
    return !flag;
};

$.fn.form.settings.rules.checkEmail = function(email){
    var flag = false;
    var data = {
        'email': email
    };
    $.ajax({
        async : false,
        url: '/auth/check_email',
        type: "POST",
        data: JSON.stringify(data),
        dataType   : "json",
        success: function(ret){
            flag = ret["detail"];
        }
    });
    return !flag;
};

$('#register_form').form({
    username: {
        identifier: 'username',
        rules: [
            {
                type: 'empty',
                prompt: '请输入用户名'
            },
            {
                type: 'checkUsernameFormat',
                prompt: '用户名必须是6-20位字母和数字的组合, 第一位必须为字母'
            },
            {
                type: 'checkUsername',
                prompt: '用户名已经存在'
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
    },
    email: {
        identifier: 'email',
        rules: [
            {
                type: 'empty',
                prompt: '请输入邮箱'
            },
            {
                type: 'email',
                prompt: '邮箱格式错误'
            },
            {
                type: 'checkEmail',
                prompt: '邮箱已存在'
            }
        ]
    }
}, {
    on: 'submit',
    inline: true
});

$('#register').click(function () {
    $('#register_form').submit();
});

$('#reset_register').click(function () {
    $('#register_form').form('reset');
});