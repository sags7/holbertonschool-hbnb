import { getCookie } from './scripts.js';


document.addEventListener('DOMContentLoaded', () => {
  const priceFilter = document.getElementById('price-filter');
  const placesList = document.querySelector('#places-list ul');
  const maxPrices = ["All", 100, 200, 300, 400, 500, 1000];
  const loginButton = document.getElementById('login-link');
  let selectedMax = maxPrices[maxPrices.length - 1];
  let placesData = [];

  const token = getCookie('token');

  if (token && loginButton) {
    loginButton.textContent = 'Logout';
  }

  maxPrices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = `$${price}`;
    priceFilter.appendChild(option);
  });



  fetch('http://127.0.0.1:5000/api/v1/places')
    .then(response => {
      if (!response.ok) throw new Error('Could not fetch places');
      return response.json();
    })
    .then(data => {
      placesData = data;
      renderPlaces(placesData);
    })
    .catch(error => {
      console.error('Error fetching places:', error);
    });

  priceFilter.addEventListener('change', () => {
    selectedMax = parseInt(priceFilter.value);
    if (isNaN(selectedMax)) selectedMax = maxPrices[maxPrices.length - 1];

    const filtered = placesData.filter(place => place.price <= selectedMax);
    renderPlaces(filtered);
  });

  function renderPlaces(places) {
    placesList.innerHTML = '';
    places.forEach(place => {
      const li = document.createElement('li');
      li.classList.add('place-card');

      li.innerHTML = `
        <h3>${place.title}</h3>
        <p><strong>Price:</strong> ${place.price}</p>
        <p>${place.description}</p>
        <a href="./html/place.html?id=${place.id}" class="details-button">View Details</a>
      `;
      placesList.appendChild(li);
    });
  }
});
