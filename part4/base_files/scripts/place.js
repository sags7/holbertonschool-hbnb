
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');

  if (!placeId) document.getElementById('place-title').textContent = 'Place not found';

  fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
    .then(response => {
      if (!response.ok) throw new Error('Could not fetch place details');
      return response.json();
    })
    .then(data => {
      document.getElementById('place-title')
        .textContent = data.title;
      document.getElementById('place-host')
        .innerHTML = `<div><p><strong>Host:</strong> ${data.owner.first_name} ${data.owner.last_name}</p></div>`;
      document.getElementById('place-price')
        .innerHTML = `<div><p><strong>Price:</strong> $${data.price}</p></div>`;
      document.getElementById('place-details')
        .innerHTML = `<div><p>${data.description}</p></div>`;

    })
});

