document.addEventListener('DOMContentLoaded', function () {
  // Load header and footer
  fetch("partials/nav_bar.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("header").innerHTML = data;
    })
    .catch((error) => console.error("Error loading header:", error));

  fetch("partials/footer.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("footer").innerHTML = data;
      document.querySelector('main').style.display = 'block';
    });

  // Initialize variables
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-link');

  // Check if user is logged in and log out if so
  if (loginButton) document.cookie = "token=; Max-Age=0; path=/;";

  // Handle the login form submission
  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!email || !password) {
        errorMessage.innerHTML = `<p>Please enter both email and password.</p>`;
        return;
      }

      signUpUser(email, password)
        .then((response) => {
          if (!response.ok) {
            errorMessage.innerHTML = `<p>Login failed: Invalid credentials or server error.</p>`;
            throw new Error('Login failed');
          }
          return response.json();
        })
        .then((data) => {
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = '../html/index.html';
        })
        .catch((error) => {
          console.error('Login error:', error);
          errorMessage.innerHTML = `<p>Login failed: Invalid credentials or server error.</p>`;
        });
    });
  }
});

// Function to sign up the user via the api
function signUpUser(email, password) {
  return fetch('http://127.0.0.1:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email, password: password })
  });
}
