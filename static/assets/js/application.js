$(document).ready(function() {
    $('.stripe-button-el').addClass('btn-stripe btn-upper btn btn-primary checkout-page-button')
    $('.stripe-button-el').removeClass('stripe-button-el')
    $('.payment_btn_div button').addClass('disabled');
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
    $('#address_textarea').change(function() {
        if ($(this).val() != '') {
            $('.payment_btn_div button').removeClass('disabled');
            $('.btn-checkout').removeClass('disabled');
        } else {
            $('.payment_btn_div button').addClass('disabled');
            $('.btn-checkout').addClass('disabled');
        }
    })

    $('.btn-checkout').click(function() {
        $('#payment-form').submit();
    });
});