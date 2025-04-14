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

  // Initialize variables
  const token = getCookie('token');
  let userId = null;

  // Check if user is logged in
  if (token) {
    userId = parseJwt(token).sub.id ? parseJwt(token).sub.id : null;
  }
  else window.location.href = '../html/index.html';

  document.querySelector('#post-amenity-button').addEventListener('click', function (event) {
    event.preventDefault();
    const amenityName = document.querySelector('#amenity-name').value;
    if (amenityName) {
      submitAmenity(amenityName)
        .then(response => {
          if (response.ok) {
            document.querySelector('#amenity-name').value = 'Amenity added!';
            window.location.href = '../html/index.html';
            document.querySelector('#post-amenity-button').style.display = 'none';
          } else {
            alert('Failed to add amenity. Please try again.');
          }
        })
        .catch(error => console.error('Error adding amenity:', error));
    }
  });

  function submitAmenity(name) {
    return fetch('http://127.0.0.1:5000/api/v1/amenities', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name: name
      })
    });
  }

});
