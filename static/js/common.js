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