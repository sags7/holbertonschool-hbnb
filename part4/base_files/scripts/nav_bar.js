import { getCookie, parseJwt } from "./scripts.js";

const token = getCookie('token');
const loginButton = document.getElementById('login-link');

loginButton.href = '../html/login-signup.html';

if (loginButton && token) {
  loginButton.textContent = 'Profile';


  loginButton.addEventListener('click', (event) => {
    event.preventDefault();

    if (token && loginButton) {
      loginButton.href = '../html/profile.html';
      window.location.href = loginButton.href;
    }
  });
}


