// This script manages the document list and logout functionality.

document.addEventListener('DOMContentLoaded', function () {
  fetch('https://IvanG-Prog-facial-recognition.hf.space/documents')
    .then(response => response.json())
    .then(data => {
      // Handle the document data here
      const documentList = document.getElementById('documentList');
      data.documents.forEach(doc => {
        const listItem = document.createElement('li');
        listItem.textContent = doc.title;
        documentList.appendChild(listItem);
      });
    })
    .catch(error => {
      console.error('Error fetching documents:', error);
    });

  const logoutBtn = document.querySelector('.btn-logout');
  if (logoutBtn) {
    logoutBtn.onclick = function () {
      window.location.href = '/';
    };
  }
});
