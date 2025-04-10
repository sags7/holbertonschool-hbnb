document.addEventListener('DOMContentLoaded', function () {
  const signupForm = document.getElementById('signup-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-link');

  if (loginButton) document.cookie = "token=; Max-Age=0; path=/;";

  if (signupForm) {
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const firstName = document.getElementById('first-name').value.trim();
      const lastName = document.getElementById('last-name').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      let is_admin = false;

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
          // Redirect to login or home if successful
          window.location.href = '../html/login.html';
        })
        .catch((error) => {
          console.error('Signup error:', error.message);
        });
    });
  }
});

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
