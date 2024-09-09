document.getElementById('status').addEventListener('change', function() {
    var priceLabel = document.getElementById('priceLabel');
    if (this.value === 'rent') {
        priceLabel.textContent = 'Price per month';
    } else {
        priceLabel.textContent = 'Price';
    }
});

function showImagesModal(flatId, image1, image2, image3) {
    // Generate image URLs
    const baseUrl = '/static/images/';
    const images = [image1, image2, image3].filter(image => image); // Filter out null/undefined

    const carouselInner = document.getElementById('carouselImages');
    carouselInner.innerHTML = '';  // Clear existing images

    images.forEach((imageSrc, index) => {
        const isActive = index === 0 ? 'active' : '';  // Set the first image as active
        const carouselItem = `
            <div class="carousel-item ${isActive}">
                <img src="${baseUrl}${imageSrc}" class="d-block w-100" alt="Flat Image ${index + 1}">
            </div>
        `;
        carouselInner.insertAdjacentHTML('beforeend', carouselItem);
    });

    // Show the modal
    const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
    imageModal.show();
}

function editFlat(id) {
    // Implement the edit functionality here
    console.log('Edit flat with ID:', id);
}

function deleteFlat(id) {
    if (confirm('Are you sure you want to delete this flat?')) {
        fetch(`/flats/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload(); // Reload the page to see changes
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function openEditModal(id, city, location, address, status, price, image1, image2, image3, description) {
        document.getElementById('editFlatId').value = id;
        document.getElementById('editCity').value = city;
        document.getElementById('editLocation').value = location;
        document.getElementById('editAddress').value = address;
        document.getElementById('editStatus').value = status;
        document.getElementById('editPrice').value = price;
        document.getElementById('editDescription').value = description;

        new bootstrap.Modal(document.getElementById('editFlatModal')).show();
}

async function updateFlat() {
    const form = document.getElementById('editFlatForm');
    const formData = new FormData(form);

    // Log form data entries
    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`);
    });

    const flatId = formData.get('id');

    try {
        const response = await fetch(`/flats/${flatId}`, {
            method: 'PUT',
            body: formData // FormData will handle its own content type
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const result = await response.json();
        alert(result.message);
        location.reload(); // Reload the page to see the updated data
    } catch (error) {
        console.error('Error:', error);
    }
}
