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