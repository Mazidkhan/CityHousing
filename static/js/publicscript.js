var registerPopup = document.getElementById('register-popup');
var registerBtn = document.getElementById('register-btn');
var closeBtn = document.querySelector('.close-btn');

// Show the popup when "Register" is clicked
registerBtn.addEventListener('click', function() {
  registerPopup.style.display = 'flex'; // Use flex to center the popup
});

// Close the popup when the close button is clicked
closeBtn.addEventListener('click', function() {
  registerPopup.style.display = 'none';
});

// Close the popup when clicking outside the popup content
window.addEventListener('click', function(event) {
  if (event.target == registerPopup) {
    registerPopup.style.display = 'none';
  }
});

document.addEventListener('DOMContentLoaded', function() {
  const citySelect = document.getElementById('citySelect');
  const locationSelect = document.getElementById('locationSelect');

  citySelect.addEventListener('change', function() {
    const selectedCity = citySelect.value;

    // Enable or disable the location dropdown based on city selection
    if (selectedCity) {
      locationSelect.disabled = false;
    } else {
      locationSelect.disabled = true;
      locationSelect.value = ''; // Reset location selection if no city is selected
    }

    // Show all locations if no city is selected
    if (!selectedCity) {
      for (const option of locationSelect.options) {
        option.style.display = 'block';
      }
      return;
    }

    // Hide locations that do not match the selected city
    for (const option of locationSelect.options) {
      if (option.dataset.city === selectedCity) {
        option.style.display = 'block';
      } else {
        option.style.display = 'none';
      }
    }

    // Reset location selection
    locationSelect.value = '';
  });
});
