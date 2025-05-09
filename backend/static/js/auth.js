document.addEventListener('DOMContentLoaded', function() {

    // Register form tab handling
    const tabButtons = document.querySelectorAll('.tab-btn');
    const registerForms = document.querySelectorAll('.register-form');
    
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all tabs
                tabButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Hide all forms
                registerForms.forEach(form => form.style.display = 'none');
                
                // Show the selected form
                const tabName = this.getAttribute('data-tab');
                document.getElementById(`${tabName.toLowerCase()}-form`).style.display = 'block';
            });
        });
    }
});