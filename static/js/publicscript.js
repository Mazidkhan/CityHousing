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
