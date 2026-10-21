// Client side scripts for Project Management System
document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alerts after 5 seconds if marked
  const alerts = document.querySelectorAll('.alert-auto-dismiss');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});
