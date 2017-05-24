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