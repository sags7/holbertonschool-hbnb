export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return null;
}

export function parseJwt(token) {
  try {
    const base64Payload = token.split('.')[1];
    const decodedPayload = atob(base64Payload);
    return JSON.parse(decodedPayload);
  } catch (e) {
    console.error('Invalid token:', e);
    return null;
  }
}

export function updateStars(value) {
  const filledStar = '\u2605'; // ★
  const emptyStar = '\u2606'; // ☆
  const stars = filledStar.repeat(value) + emptyStar.repeat(5 - value);
  return stars;
}