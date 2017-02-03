var limit_word_count = 140;

function word_calculator(){
    var content = ue.getContentTxt();
    // 计算字符数
    var content_html = ue.getContent();
    var img_list = content_html.match(/<img[^>]+>/g);
    var count = 0;
    if(img_list){
        count = content.length + img_list.length;
    } else {
        count = content.length
    }
    return count
}

function show_word_count(){
    var count = word_calculator();
    // 设置显示
    if(limit_word_count < count){
        $('#word_count').empty().append('<a class="ui label" style="color:#ff565d"><i class="calculator icon"></i>'+count+'/'+limit_word_count+' 超出字数限制</a>')
    } else {
        $('#word_count').empty().append('<a class="ui label"><i class="calculator icon"></i>'+count+'/'+limit_word_count+'</a>')
    }
}

var ue = UE.getEditor('ueditor-container');
ue.addListener("keyup", show_word_count);


