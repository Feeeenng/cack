$('.accordion').accordion({
    selector: {
        trigger: '.title'
    }
});

$('.ui.checkbox').checkbox();

function removeVoteData() {
    
}

function submitVoteData() {

}

$('#add-vote-modal').modal({
    transition: 'vertical flip',
    onShow: removeVoteData,
    onApprove: submitVoteData,
    allowMultiple: false
}).modal('attach events', '#add-vote', 'show');

$('#add-vote-image').dimmer({on: 'hover'});

$('#add-vote-option').click(function () {
    var option_input = $('#option-input');
    var option = option_input.val();
    if(option){
        $('#option-list').append(
            '<a class="ui teal option-label label" style="margin-top: 5px" title="' + option + '">' +
                option +
                '<input type="hidden" name="options[]" value="' + option + '">' +
                '<i class="delete icon" onclick="$(this).parent().remove()"></i>' +
            '</a>');
        option_input.val('');
    }
});

$('#vote-description').keyup(function () {
    var count = $(this).val().length;
    var vote_description_count = $('#vote-description-count');
    vote_description_count.text(count + '/256');
    if(count > 256){
        vote_description_count.addClass('beyond-count');
    } else {
        vote_description_count.removeClass('beyond-count');
    }
});