document.addEventListener('DOMContentLoaded', function() {
    // JS to show the correct payment button for Razorpay/PayPal/No Payment
    const razorpayRadio = document.getElementById('razorpay-radio');
    const paypalRadio = document.getElementById('paypal-radio');
    const noPaymentRadio = document.getElementById('no-payment-radio');

    const razorpayBtn = document.querySelector('.razorpay-btn');
    const paypalBtn = document.querySelector('.paypal-btn');
    const noPaymentBtn = document.querySelector('.no-payment-btn');

    function updateButtonVisibility() {
        if (razorpayRadio && razorpayRadio.checked) {
            if (razorpayBtn) razorpayBtn.style.display = 'inline-block';
            if (paypalBtn) paypalBtn.style.display = 'none';
            if (noPaymentBtn) noPaymentBtn.style.display = 'none';
        } else if (paypalRadio && paypalRadio.checked) {
            if (razorpayBtn) razorpayBtn.style.display = 'none';
            if (paypalBtn) paypalBtn.style.display = 'inline-block';
            if (noPaymentBtn) noPaymentBtn.style.display = 'none';
        } else if (noPaymentRadio && noPaymentRadio.checked) {
            if (razorpayBtn) razorpayBtn.style.display = 'none';
            if (paypalBtn) paypalBtn.style.display = 'none';
            if (noPaymentBtn) noPaymentBtn.style.display = 'block';
        }
    }

    if (razorpayRadio) razorpayRadio.addEventListener('change', updateButtonVisibility);
    if (paypalRadio) paypalRadio.addEventListener('change', updateButtonVisibility);
    if (noPaymentRadio) noPaymentRadio.addEventListener('change', updateButtonVisibility);

    updateButtonVisibility(); // Initial call to set the correct visibility
});
