import { getCookie, parseJwt } from "../scripts/scripts.js";

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
  if (token) userId = parseJwt(token).sub.id ? parseJwt(token).sub.id : null;
  else window.location.href = '../html/index.html';


  // populates the profile page with user details
  if (userId) {
    fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`)
      .then(response => {
        if (!response.ok) throw new Error('Could not fetch user details');
        return response.json();
      })
      .then(data => {
        console.log(data);
        document.getElementById('profile-body').innerHTML = `
        <div id="user-name"><p>${data.first_name} ${data.last_name}</p></div>
        <div id="user-email"><p>${data.email}</p></div>
        <div id="logout-button">
          <button>Logout</button>
        </div>
        `;

        document.querySelector('#logout-button button').addEventListener('click', function () {
          document.cookie = "token=; Max-Age=0; path=/;";
          window.location.href = '../html/index.html';
        });
      });
  }
});
