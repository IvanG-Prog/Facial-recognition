let streamActive = false;

function startCamera() {
  const video = document.getElementById('video');
  video.style.display = 'block';
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      streamActive = true;
      document.getElementById('msg').innerText = "Press Enter to take the photo and register.";
    })
    .catch(function (err) {
      alert('The camera could not be accessed: ' + err);
    });
}

document.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    if (streamActive) {
      event.preventDefault();
      takePhotoAndRecord();
    }
  }
});

function validateAndActivate() {
  const form = document.getElementById('registroForm');
  const name = form.name.value.trim();
  const lastName = form.lastname.value.trim();
  const id = form.id.value.trim();
  const username = form.username.value.trim();

  if (!name || !lastName || !id || !username) {
    alert("Please fill in all fields before activating the camera.");
    return;
  }

  const numbersOnly = /^\d+$/;
  const lettersAndSpaces = /^[A-Za-z\s]+$/;
  const validUsername = /^[A-Za-z0-9!@#\$%\^&\*\-_\+=\{\}\[\]\(\)\|\\:;'<>,\.\?\/]+$/;

  if (!name.match(lettersAndSpaces)) {
    alert("Name must contain only letters and spaces.");
    return;
  }
  if (!lastName.match(lettersAndSpaces)) {
    alert("Last name must contain only letters and spaces.");
    return;
  }
  if (!id.match(numbersOnly)) {
    alert("ID must contain only numbers.");
    return;
  }
  if (!username.match(validUsername)) {
    alert("Username can contain letters, numbers, and allowed special characters.");
    return;
  }

  fetch('https://IvanG-Prog-facial-recognition.hf.space/check_username', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username })
  })
    .then(response => response.json())
    .then(data => {
      if (data.available) {
        startCamera();
      } else {
        alert(data.message);
      }
    })
    .catch(err => alert('Error checking username: ' + err));
}

function takePhotoAndRecord() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imagenBase64 = canvas.toDataURL('image/png');
  register(imagenBase64);
}

function register(imagenBase64) {
  const form = document.getElementById('registroForm');
  if (!form.name.value || !form.lastname.value || !form.id.value || !form.username.value) {
    alert('Please fill in all fields before taking the photo.');
    return;
  }
  const datos = {
    name: form.name.value,
    "last name": form.lastname.value,
    id: form.id.value,
    username: form.username.value,
    image: imagenBase64
  };
  fetch('https://IvanG-Prog-facial-recognition.hf.space/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  }).then(response => response.json())
    .then(data => {
      alert(data.message);
      const video = document.getElementById('video');
      if (video && video.srcObject) {
        let tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
      }
      if (data.status === "ok" || data.status === "face_exists") {
        window.location.href = "/";
      }
    })
    .catch(err => alert('Error: ' + err));
}
