// script.js - Client-side JavaScript for Turbo Financials Form Handler

// Form validation and enhancement functions

/**
 * Validates email format
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if valid email format
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Formats phone number as user types
 * @param {HTMLInputElement} input - Phone input element
 */
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 10) {
        value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    }
    input.value = value;
}

/**
 * Masks SSN input (shows only last 4 digits)
 * @param {HTMLInputElement} input - SSN input element
 */
function maskSSN(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 4) {
        value = 'XXX-XX-' + value.slice(-4);
    }
    input.value = value;
}

/**
 * Validates form before submission
 * @param {HTMLFormElement} form - Form element to validate
 * @returns {boolean} - True if form is valid
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }

        // Email validation
        if (field.type === 'email' && field.value) {
            if (!validateEmail(field.value)) {
                field.classList.add('error');
                isValid = false;
            }
        }
    });

    return isValid;
}

/**
 * Shows loading state during form submission
 * @param {HTMLButtonElement} submitBtn - Submit button element
 * @param {boolean} isLoading - Whether to show loading state
 */
function setLoadingState(submitBtn, isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';
        submitBtn.classList.add('loading');
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
        submitBtn.classList.remove('loading');
    }
}

/**
 * Shows success message after form submission
 * @param {string} message - Success message to display
 */
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => successDiv.remove(), 300);
    }, 3000);
}

/**
 * Handles form submission with validation and loading states
 * @param {Event} event - Form submit event
 */
function handleFormSubmit(event) {
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    // Validate form
    if (!validateForm(form)) {
        event.preventDefault();
        alert('Please fill in all required fields correctly.');
        return;
    }

    // Show loading state
    setLoadingState(submitBtn, true);

    // For traditional form submission, this will proceed normally
    // If you want AJAX submission, uncomment the code below and prevent default

    /*
    event.preventDefault();

    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        setLoadingState(submitBtn, false);
        if (data.success) {
            showSuccessMessage('Form submitted successfully!');
            form.reset();
        } else {
            alert('Error submitting form. Please try again.');
        }
    })
    .catch(error => {
        setLoadingState(submitBtn, false);
        alert('Network error. Please check your connection and try again.');
        console.error('Form submission error:', error);
    });
    */
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });

    // SSN masking
    const ssnInputs = document.querySelectorAll('input[name*="ssn"], input[name*="SSN"]');
    ssnInputs.forEach(input => {
        input.addEventListener('input', function() {
            maskSSN(this);
        });
    });

    // Form validation on submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });

    // Real-time validation feedback
    const requiredInputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }

            if (this.type === 'email' && this.value) {
                if (!validateEmail(this.value)) {
                    this.classList.add('error');
                } else {
                    this.classList.remove('error');
                }
            }
        });
    });
});

// CSS for error states and animations (add to your CSS file)
const style = document.createElement('style');
style.textContent = `
    .error {
        border-color: #ff4444 !important;
        box-shadow: 0 0 5px rgba(255, 68, 68, 0.3) !important;
    }

    .loading {
        opacity: 0.7;
        cursor: not-allowed;
    }

    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);