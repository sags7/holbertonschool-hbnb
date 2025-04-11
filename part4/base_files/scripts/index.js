import { getCookie } from '../scripts/scripts.js';


document.addEventListener('DOMContentLoaded', () => {
  fetch("./partials/nav_bar.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("header").innerHTML = data;
    })
    .catch((error) => console.error("Error loading header:", error));

  fetch("./partials/footer.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("footer").innerHTML = data;
      document.querySelector('main').style.display = 'block';
    });



  const priceFilter = document.getElementById('price-filter');
  const placesList = document.querySelector('#places-list ul');
  const maxPrices = ["All", 100000, 200000, 300000, 400000, 500000, 1000000];
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
        <a href="./place.html?id=${place.id}" class="details-button">View Details</a>
      `;
      placesList.appendChild(li);
    });
  }
});
