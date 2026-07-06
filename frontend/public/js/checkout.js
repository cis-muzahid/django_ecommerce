document.addEventListener('DOMContentLoaded', function() {
    var useDefaultAddressButton = document.getElementById('use-default-address');
    var addNewAddressButton = document.getElementById('add-new-address');
    var addressForm = document.getElementById('address-div');

    if (useDefaultAddressButton) {
        useDefaultAddressButton.addEventListener('click', function() {
            alert('Using default address for your order.');
            window.location.href = '/checkout/';  // Redirect to the checkout page or handle as needed
        });
    }

    if (addNewAddressButton) {
        addNewAddressButton.addEventListener('click', function() {
            addressForm.style.display = 'block';
            document.getElementById('default-address-div').style.display = "None"
        });
    }

    if (addressForm) {
        addressForm.style.display = 'none';
    }
    });

    document.getElementById('new_address_div').style.display = 'none';
    document.getElementById('new-address').addEventListener('click', function(){
    document.getElementById('address_form_div').style.display = 'none';
    document.getElementById('new_address_div').style.display = 'block';

    const streetInput = document.getElementById('street');
    const cityInput = document.getElementById('city');
    const stateInput = document.getElementById('state');
    const postalCodeInput = document.getElementById('postal_code');
    const countryInput = document.getElementById('country');
    const combinedAddressInput = document.getElementById('address_input');

    // Function to update the combined address input field
    function updateCombinedAddress() {
    const street = streetInput.value.trim();
    const city = cityInput.value.trim();
    const state = stateInput.value.trim();
    const postalCode = postalCodeInput.value.trim();
    const country = countryInput.value.trim();

    const combinedAddress = [street, city, state, postalCode, country].filter(Boolean).join(', ');
    console.log(combinedAddress)
    combinedAddressInput.value = combinedAddress;
    }

    // Add event listeners to all input fields to update the combined address
    streetInput.addEventListener('input', updateCombinedAddress);
    cityInput.addEventListener('input', updateCombinedAddress);
    stateInput.addEventListener('input', updateCombinedAddress);
    postalCodeInput.addEventListener('input', updateCombinedAddress);
    countryInput.addEventListener('input', updateCombinedAddress);

    // Initial call to set the combined address if any fields are pre-filled
    updateCombinedAddress();
});



function change_address(address) {
    console.log('Selected address:', address);
    addressInput = document.getElementById('address_input')
    addressInput.value = address.street + ', ' + address.city + ', ' +  address.state + ', '  + address.postal_code + ', ' + address.country
}

document.getElementById('paypalForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Submit the form using JavaScript
    fetch(this.action, {
        method: this.method,
        body: new FormData(this), // Include form data in the request
    })
    .then(response => response.json())
    .then(data => {
        // Redirect to the PayPal approval URL
        window.location.href = data.approval_url;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle any errors
    });
});


