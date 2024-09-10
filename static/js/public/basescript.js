document.addEventListener('DOMContentLoaded', () => {
    const citySelect = document.getElementById('citySelect');
    const locationSelect = document.getElementById('locationSelect');

    if (typeof window.flatsFilter === 'undefined') {
        console.error('flatsFilter data not found.');
        return;
    }

    citySelect.addEventListener('change', function() {
        const selectedCity = this.value;
        locationSelect.innerHTML = '<option value="">Location</option>';
        if (selectedCity) {
            const locations = window.flatsFilter.filter(flat => flat[0] === selectedCity).map(flat => flat[1]);
            if (locations.length > 0) {
                locationSelect.disabled = false;
                locations.forEach(location => {
                    const option = document.createElement('option');
                    option.value = location;
                    option.textContent = location;
                    locationSelect.appendChild(option);
                });
            } else {
                locationSelect.disabled = true;
            }
        } else {
            locationSelect.disabled = true;
        }
    });
});
