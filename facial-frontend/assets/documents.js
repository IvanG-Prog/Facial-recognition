// This script manages the document list and logout functionality.

document.addEventListener('DOMContentLoaded', function () {
  const logoutBtn = document.querySelector('.btn-logout');
  if (logoutBtn) {
    logoutBtn.onclick = function () {
      window.location.href = '/';
    };
  }
});
