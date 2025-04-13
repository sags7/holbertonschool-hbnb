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
    window.location.href = '../html/index.html';
});
