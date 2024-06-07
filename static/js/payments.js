document.addEventListener('DOMContentLoaded', function() {
    // JS to show diverse payment button
    const stripeRadio = document.getElementById('stripe-radio');
    const paypalRadio = document.getElementById('paypal-radio');
    const noPaymentRadio = document.getElementById('no-payment-radio');

    const stripeBtn = document.querySelector('.stripe-btn');
    const paypalBtn = document.querySelector('.paypal-btn');
    const noPaymentBtn = document.querySelector('.no-payment-btn');

    function updateButtonVisibility() {
        if (stripeRadio.checked) {
        stripeBtn.style.display = 'inline-block';
        paypalBtn.style.display = 'none';
        noPaymentBtn.style.display = 'none';
        } else if (paypalRadio.checked) {
        stripeBtn.style.display = 'none';
        paypalBtn.style.display = 'inline-block';
        noPaymentBtn.style.display = 'none';
        } else if (noPaymentRadio.checked) {
        stripeBtn.style.display = 'none';
        paypalBtn.style.display = 'none';
        noPaymentBtn.style.display = 'block';
        }
    }

    stripeRadio.addEventListener('change', updateButtonVisibility);
    paypalRadio.addEventListener('change', updateButtonVisibility);
    noPaymentRadio.addEventListener('change', updateButtonVisibility);

    updateButtonVisibility(); // Initial call to set the correct visibility
});
