document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('register-btn').onclick = function () {
    fetch('https://IvanG-Prog-facial-recognition.hf.space/check_username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'test' }) // Cambia 'test' por el valor real si lo tienes
    })
      .then(response => {
        if (response.ok) {
          window.location.href = 'register.html';
        } else {
          alert('Registration failed. Please try again.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      });
  };
  document.getElementById('access-btn').onclick = function () {
    fetch('https://IvanG-Prog-facial-recognition.hf.space/check_username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'test' }) // Cambia 'test' por el valor real si lo tienes
    })
      .then(response => {
        if (response.ok) {
          window.location.href = 'access.html';
        } else {
          alert('Access denied. Please try again.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      });
  };
});
