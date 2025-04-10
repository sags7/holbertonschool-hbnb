document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-link');

  if (loginButton) document.cookie = "token=; Max-Age=0; path=/;";


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
          window.location.href = '../index.html';
        })
        .catch((error) => {
          console.error('Login error:', error);
          errorMessage.innerHTML = `<p>Login failed: Invalid credentials or server error.</p>`;
        });
    });
  }
});

function signUpUser(email, password) {
  return fetch('http://127.0.0.1:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email, password: password })
  });
}
