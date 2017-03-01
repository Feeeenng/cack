function checkEmailFormat(email) {
    // 检查邮箱
    var reg = /\w+[@]{1}\w+[.]\w+/;
    return reg.test(email)
}