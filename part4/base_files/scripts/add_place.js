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
  console.log(userId);

  // Check if user is logged in
  if (token) userId = parseJwt(token).sub.id ? parseJwt(token).sub.id : null;
  else window.location.href = '../html/index.html';

  document.getElementById('submit-button').addEventListener('click', function (event) {
    submitPlace(
      document.getElementById('title').value.trim(),
      document.getElementById('description').value.trim(),
      document.getElementById('price').value.trim(),
      document.getElementById('latitude').value.trim(),
      document.getElementById('longitude').value.trim(),
      userId
    ).then(response => {
      if (response.ok) {
        window.location.href = '../html/index.html';
      } else {
        console.error('Error submitting place:', response.statusText);
      }
    }).catch(error => {
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
});
