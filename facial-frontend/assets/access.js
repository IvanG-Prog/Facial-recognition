function validateAndStartCamera() {
  const form = document.getElementById('accessForm');
  const username = form.username.value.trim();
  const ssnn = form.ssnn.value.trim();

  if (!username || !ssnn) {
    alert("Please fill in both Username and SSNN before activating the camera.");
    return;
  }

  const numbersOnly = /^\d+$/;
  if (!ssnn.match(numbersOnly)) {
    alert("SSNN must contain only numbers.");
    return;
  }
  fetch('https://huggingface.co/spaces/IvanG-Prog/facial-recognition.hf.space/validate_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username, ssnn: ssnn })
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "ok") {
        startCamera();
      } else {
        alert(data.message);
      }
    })
    .catch(err => alert('Error: ' + err));

}

let streamActive = false;
function startCamera() {
  const video = document.getElementById('video');
  video.style.display = 'block';
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      streamActive = true;
      document.getElementById('msg').innerText = "Press Enter to take the photo and access.";
    })
    .catch(function (err) {
      alert('The camera could not be accessed: ' + err);
    });
}

document.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    if (streamActive) {
      takePhotoAndAccess();
    }
  }
});

function takePhotoAndAccess() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageBase64 = canvas.toDataURL('image/png');
  access(imageBase64);
}

function access(imageBase64) {
  const form = document.getElementById('accessForm');
  if (!form.username.value || !form.ssnn.value) {
    alert('Please enter your username and SSNN before taking the photo.');
    return;
  }
  const data = {
    username: form.username.value,
    ssnn: form.ssnn.value,
    image: imageBase64
  };
  fetch('https://huggingface.co/spaces/IvanG-Prog/facial-recognition.hf.space/access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(response => response.json())
    .then(data => {
      alert(data.message);
      if (data.status === "ok") {
        window.location.href = "/documents";
      }
    })
    .catch(err => alert('Error: ' + err));
}
