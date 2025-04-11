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
  const signupForm = document.getElementById('signup-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-link');

  // Check if user is logged and log out if so
  if (loginButton) document.cookie = "token=; Max-Age=0; path=/;";

  // Handle the signup form submission
  if (signupForm) {
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const firstName = document.getElementById('first-name').value.trim();
      const lastName = document.getElementById('last-name').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const confirmPassword = document.getElementById('confirm-password').value.trim();
      let is_admin = false;

      if (password !== confirmPassword) {
        console.log("preventing submission")
        document.getElementById('password').value = '';
        document.getElementById('confirm-password').value = '';
        document.getElementById('password-error').innerHTML = `<p>Passwords do not match.</p>`;
        return
      }

      if (document.getElementById('dev-password').value.trim() === "True") is_admin = true;

      if (!email || !password || !firstName || !lastName) {
        errorMessage.innerHTML = `<p>Please enter name, last name, email and password.</p>`;
        return;
      }

      console.log(JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
        is_admin: is_admin
      }));

      signUpUser(firstName, lastName, email, password, is_admin)
        .then((response) => {
          if (!response.ok) {
            return response.json().then(data => {
              errorMessage.innerHTML = `<p>Signup failed: ${data.message || "An error occurred."}</p>`;
              throw new Error(data.message || 'Signup failed');
            });
          }
          return response.json();
        })
        .then((data) => {
          console.log('Signup successful:', data);
          window.location.href = '../html/login.html';
        })
        .catch((error) => {
          console.error('Signup error:', error.message);
        });
    });
  }
});

// Function to sign up a user via the api
function signUpUser(firstName, lastName, email, password, isAdmin) {
  return fetch('http://127.0.0.1:5000/api/v1/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      is_admin: isAdmin
    })
  });
}
