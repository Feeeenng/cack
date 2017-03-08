function checkEmailFormat(email) {
    // 检查邮箱
    var reg = /\w+[@]{1}\w+[.]\w+/;
    return reg.test(email)
}

function errorPrompt(filed_name, error_msg) {
    $('input[name="'+filed_name+'"]').focus();
    $('input[name="'+filed_name+'"]').parent().popup({
        position : 'left center',
        title    : error_msg,
        duration : 100
    }).popup('toggle');
}

function blurRemoveErrorPrompt(obj) {
    $(obj).parent().popup('destroy');
}

function lockButton(obj, content){
    //验证码
    var s = 59;
    var _this = $(obj);
    _this.addClass('disabled').html('Send again ('+ s +'s)');
    var timer = setInterval(function(){
        s--;
        _this.html('Send again ('+ s +'s)');
        if(s == 0){
            _this.removeClass('disabled').html(content);
            clearInterval(timer);
        }
    },1000);
}

$('.message .close').on('click', function() {
    // 关闭消息
    $(this).closest('.message').transition('fade');
});

function showSentEmailMessage() {
    // 展示发送邮件后的消息
    var x = function () {
        $('#loading_message').transition('swing down', '2s');
    };
    $('#loading_message').transition('swing down', '2s', function(){
        setTimeout(x, 5000)
    })
}

function messageTips(id, msg, action, seconds) {
    $('#'+id).html(msg);
    var x = function () {
        $('#'+id).transition(action, seconds);
    };
    $('#'+id).transition(action, seconds, function(){
        setTimeout(x, 5000)
    })
}