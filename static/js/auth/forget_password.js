$('#forget-password-form').form({
    username: {
        identifier: 'username',
        rules: [
            {
                type: 'empty',
                prompt: '请输入用户名'
            }
        ]
    },
    email: {
        identifier: 'email',
        rules: [
            {
                type: 'empty',
                prompt: '请输入密码'
            },
            {
                type: 'email',
                prompt: '邮箱格式错误'
            }
        ]
    }
}, {
    on: 'submit',
    inline: true,
    onSuccess: submitForgetPasswordForm
});

$('#forget-password-submit').click(function () {
    $('#forget-password-form').submit(function () {
        return false;
    });
});

function submitForgetPasswordForm() {
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