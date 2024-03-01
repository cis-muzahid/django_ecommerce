$(document).ready(function() {
    $('.plus').click(function() {
        var input = $('#quantity-input');
        var value = parseInt(input.val());
        input.val(value + 1);
    });

    $('.minus').click(function() {
        var input = $('#quantity-input');
        var value = parseInt(input.val());
        if (value > 1) {
            input.val(value - 1);
        }
    });
});