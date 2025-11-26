// Dashboard Interactivity

// User Profile Dropdown
const userProfileDropdown = document.getElementById('userProfileDropdown');
if (userProfileDropdown) {
  userProfileDropdown.addEventListener('click', function(e) {
    // Don't prevent default if clicking on logout button
    if (e.target.type === 'submit') {
      return;
    }
    e.preventDefault();
    this.classList.toggle('active');
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!userProfileDropdown.contains(e.target)) {
      userProfileDropdown.classList.remove('active');
    }
  });
}

// Wallet Tab Switching
document.querySelectorAll('.wallet-tab').forEach(tab => {
  tab.addEventListener('click', function() {
    // Remove active class from all tabs
    document.querySelectorAll('.wallet-tab').forEach(t => t.classList.remove('active'));
    // Add active class to clicked tab
    this.classList.add('active');
  });
});

// Sidebar Navigation
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', function(e) {
    // Remove active class from all items
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    // Add active class to clicked item
    this.classList.add('active');
  });
});

// Action Buttons
document.querySelectorAll('.action-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const action = this.querySelector('.action-label').textContent;
    console.log('Action clicked:', action);
    // Add action handlers here
  });
});

// Card Edit Buttons
document.querySelectorAll('.card-edit').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    console.log('Edit card');
    // Add edit functionality here
  });
});

// Storage Chart Segments
document.querySelectorAll('.chart-segment').forEach(segment => {
  segment.addEventListener('click', function() {
    console.log('Chart segment clicked');
    // Add chart interaction here
  });
});

// Buy Storage Button
const buyStorageBtn = document.querySelector('.buy-storage-btn');
if (buyStorageBtn) {
  buyStorageBtn.addEventListener('click', function() {
    alert('Storage upgrade feature coming soon!');
  });
}

// Transaction Row Click
document.querySelectorAll('.transaction-item').forEach(row => {
  if (!row.classList.contains('billing-plan-item')) {
    row.addEventListener('click', function() {
      console.log('Transaction row clicked');
      // Add row interaction here
    });
  }
});

console.log('Dashboard initialized');
