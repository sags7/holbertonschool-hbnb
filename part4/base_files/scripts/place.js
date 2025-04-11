import { getCookie, parseJwt, updateStars } from './scripts.js';

document.addEventListener('DOMContentLoaded', () => {
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

  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');
  const loginButton = document.getElementById('login-link');
  const token = getCookie('token');
  const ratingInput = document.getElementById('rating');
  const starDisplay = document.getElementById('star-display');
  let ownerId = null;
  let userId = null;

  if (token) {
    userId = parseJwt(token).sub.id ? parseJwt(token).sub.id : null;
  }
  /*const submitReviewBtn = document.querySelector('review-form button[type="submit"]');*/

  if (!token) document.getElementById('add-review').innerHTML = `<h2><a href="./login.html" id="login-link">Login to add a review</a></h2>`;
  if (token && loginButton) loginButton.textContent = 'Logout';
  if (!placeId) document.getElementById('place-title').textContent = 'Place not found';

  fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
    .then(response => {
      if (!response.ok) throw new Error('Could not fetch place details');
      return response.json();
    })
    .then(data => {
      ownerId = data.owner.id;
      document.getElementById('place-title')
        .textContent = data.title;
      document.getElementById('place-host')
        .innerHTML = `<div><p><strong>Host:</strong> ${data.owner.first_name} ${data.owner.last_name}</p></div>`;
      document.getElementById('place-price')
        .innerHTML = `<div><p><strong>Price:</strong> $${data.price}</p></div>`;
      document.getElementById('place-details')
        .innerHTML = `<div><p>${data.description}</p></div>`;
    })
    .then(() => {
      fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
        .then(response => {
          if (!response.ok) throw new Error('Could not fetch reviews');
          return response.json();
        })
        .then((data) => {
          data.forEach(element => {
            renderReviewCard(element);
          });
        });
    });

  function renderReviewCard(review) {
    const reviewCard = document.createElement('div');
    reviewCard.classList.add('review-card');
    reviewCard.innerHTML = `
      <h3><strong>Review:</strong> ${review.rating}</h3>
      <p>${review.text}</p>
    `;
    document.getElementById('reviews').appendChild(reviewCard);
  };

  document.addEventListener('input', (event) => {
    starDisplay.textContent = updateStars(ratingInput.value);
  });

  document.addEventListener('submit', (event) => {
    event.preventDefault();
    const reviewForm = event.target.closest('form');
    if (!reviewForm) return;
    if (ownerId !== userId) {
      fetch(`http://127.0.0.1:5000/api/v1/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getCookie('token')}`
        },
        body: JSON.stringify({
          text: reviewForm.querySelector('textarea').value,
          rating: parseInt(ratingInput.value),
          user_id: userId,
          place_id: placeId
        })
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(errData => {
              reviewForm.querySelector('textarea').value = errData.message;
              throw new Error(errData.message);
            });
          }
          return response.json();
        })
        .then(data => {
          console.log('Review submitted:');
          renderReviewCard(data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
      reviewForm.querySelector('textarea').value = `Review submitted!`;
    }
    else {
      reviewForm.querySelector('textarea').value = `You cannot review your own place`;
      alert('You cannot review your own place!');
    }
  });

});

