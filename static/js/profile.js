// user profile mobile number validation for 10 digit
useDefaultAddressButton.addEventListener('change', function() {
    mobileNumberInput = document.getElementById('mobile_number')
    if (mobileNumberInput.value.length != 10)
    {
        update_profile_button.classList.add("disabled")
        console.log(mobileNumberInput.value)
    } 
    console.log(mobileNumberInput.value.length)

});