document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('register-btn').onclick = function () {
    fetch('https://huggingface.co/spaces/IvanG-Prog/facial-recognition/api/check')
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
    fetch('https://huggingface.co/spaces/IvanG-Prog/facial-recognition/api/check')
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
