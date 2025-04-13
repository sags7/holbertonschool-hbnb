import { getCookie, parseJwt } from "./scripts.js";

document.addEventListener('DOMContentLoaded', function () {
  // Load header and footer
  fetch("./partials/nav_bar.html")
    .then((response) => response.text())
    .then((data) => {
      const header = document.getElementById("header");
      header.innerHTML = data;
      if (header) {
        const script = document.createElement("script");
        script.type = "module";
        script.src = "../scripts/nav_bar.js";
        document.body.appendChild(script);
      }
    })
    .catch((error) => console.error("Error loading header:", error));

  fetch("partials/footer.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("footer").innerHTML = data;
      document.querySelector('main').style.display = 'block';
    });

  let chosenAmenities = [];
  let newPlaceId = null;

  // Fetch available amenities
  fetch('http://127.0.0.1:5000/api/v1/amenities')
    .then(response => {
      if (!response.ok) throw new Error('Could not fetch amenities');
      return response.json();
    })
    .then(data => {
      const amenityList = document.querySelector('#amenity-list ul');

      data.forEach(amenity => {
        const checkboxId = `amenity-${amenity.id}`;

        // Append each checkbox without replacing the inner HTML
        amenityList.insertAdjacentHTML('beforeend', `
        <li>
          <input type="checkbox" name="${amenity.name}" id="${checkboxId}">
          <label for="${checkboxId}">${amenity.name}</label>
        </li>
      `);

        // Attach event listener after it's added to the DOM
        const checkbox = document.getElementById(checkboxId);
        checkbox.addEventListener('change', function () {
          if (this.checked) {
            if (!chosenAmenities.includes(amenity.id)) {
              chosenAmenities.push(amenity.id);
            }
          } else {
            const index = chosenAmenities.indexOf(amenity.id);
            if (index > -1) chosenAmenities.splice(index, 1);
          }
        });
      });
    })
    .catch(error => {
      console.error('Error fetching amenities:', error);
    });


  // Initialize variables
  const token = getCookie('token');
  let userId = null;

  // Check if user is logged in
  if (token) userId = parseJwt(token).sub.id ? parseJwt(token).sub.id : null;
  else window.location.href = '../html/index.html';

  document.getElementById('submit-button').addEventListener('click', function (event) {
    event.preventDefault();
    submitPlace(
      document.getElementById('title').value.trim(),
      document.getElementById('description').value.trim(),
      document.getElementById('price').value.trim(),
      document.getElementById('latitude').value.trim(),
      document.getElementById('longitude').value.trim(),
      userId
    )
      .then(response => {
        if (response.ok) {
          return response.json().then(data => {
            newPlaceId = data.id;
            return addAmenities(chosenAmenities);
          }).then((data) => {
            window.location.href = '../html/index.html';
          });
        } else {
          console.error('Error submitting place:', response.statusText);
        }
      })

      .catch(error => {
        console.error('Error:', error);
      });
  });


  // Function to submit place data through API
  function submitPlace(title, description, price, latitude, longitude, userId) {
    return fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        title: title,
        description: description,
        price: price,
        latitude: latitude,
        longitude: longitude,
        owner_id: userId
      })
    });
  }

  //function to update place with amenties via api
  function addAmenities(amenities) {
    return fetch(`http://127.0.0.1:5000/api/v1/places/${newPlaceId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        amenities: amenities
      })
    });
  }
});
