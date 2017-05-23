$('.accordion').accordion({
    selector: {
        trigger: '.title'
    }
});

$('.ui.checkbox').checkbox();

$('#add-vote').click(function () {
    $('#add-vote-modal').modal('show');
});
