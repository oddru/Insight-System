// Get the modal elements
const modal = document.getElementById('loginModal');
const getStartedBtn = document.getElementById('getStartedBtn');
const closeBtn = document.querySelector('.modal-close');
const modalTabs = document.querySelectorAll('.modal-tab');
const showRegisterLink = document.getElementById('showRegister');
const showLoginLink = document.getElementById('showLogin');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// Open modal when "Get Started" button is clicked
if (getStartedBtn) {
  getStartedBtn.addEventListener('click', function() {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  });
}

// Close modal when close button is clicked
if (closeBtn) {
  closeBtn.addEventListener('click', function() {
    modal.classList.remove('show');
    document.body.style.overflow = ''; // Restore scrolling
  });
}

// Close modal when clicking outside the modal content
window.addEventListener('click', function(event) {
  if (event.target === modal) {
    modal.classList.remove('show');
    document.body.style.overflow = ''; // Restore scrolling
  }
});

// Toggle between login and register forms
if (showRegisterLink) {
  showRegisterLink.addEventListener('click', function(e) {
    e.preventDefault();
    loginForm.classList.remove('active');
    registerForm.classList.add('active');
  });
}

if (showLoginLink) {
  showLoginLink.addEventListener('click', function(e) {
    e.preventDefault();
    registerForm.classList.remove('active');
    loginForm.classList.add('active');
  });
}

// Tab switching functionality
modalTabs.forEach(tab => {
  tab.addEventListener('click', function() {
    const tabName = this.getAttribute('data-tab');
    
    // Remove active class from all tabs and contents
    modalTabs.forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.modal-tab-content').forEach(content => {
      content.classList.remove('active');
    });
    
    // Add active class to clicked tab and corresponding content
    this.classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
  });
});

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape' && modal.classList.contains('show')) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
});