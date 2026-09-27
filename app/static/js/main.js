/**
 * Clinic Management System — Main JavaScript
 * University Software Engineering Project 2024
 */

'use strict';

// ================================================================
// Auto-dismiss flash alerts after 5 seconds
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            } catch (e) {
                // Alert may already be closed
            }
        }, 5000);
    });
});

// ================================================================
// Confirm before delete
// ================================================================
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item? This action cannot be undone.');
}

// ================================================================
// Add a new medicine row in the prescription form
// ================================================================
function addMedicineRow() {
    const container = document.getElementById('medicines-container');
    if (!container) return;

    const row = document.createElement('div');
    row.className = 'medicine-row mb-2';
    row.innerHTML = `
        <div class="row g-2 align-items-center">
            <div class="col-md-3">
                <input type="text" class="form-control form-control-sm" name="medicine_name"
                       required placeholder="e.g., Amoxicillin">
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control form-control-sm" name="dosage"
                       required placeholder="e.g., 500mg">
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control form-control-sm" name="frequency"
                       required placeholder="e.g., 3x daily">
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control form-control-sm" name="duration"
                       required placeholder="e.g., 7 days">
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control form-control-sm" name="item_instructions"
                       placeholder="After meals...">
            </div>
            <div class="col-md-1">
                <button type="button" class="btn btn-outline-danger btn-sm w-100"
                        onclick="removeMedicineRow(this)" title="Remove medicine">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(row);

    // Focus first input of new row
    const firstInput = row.querySelector('input');
    if (firstInput) firstInput.focus();
}

// ================================================================
// Remove a medicine row
// ================================================================
function removeMedicineRow(button) {
    const container = document.getElementById('medicines-container');
    if (!container) return;

    if (container.children.length <= 1) {
        alert('At least one medicine is required in a prescription.');
        return;
    }

    const row = button.closest('.medicine-row');
    if (row) {
        row.remove();
    }
}

// ================================================================
// Highlight active nav link
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;
    document.querySelectorAll('.navbar .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });
});

// ================================================================
// Confirm form submit for delete buttons
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[data-confirm]').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const msg = form.getAttribute('data-confirm');
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });
});

// ================================================================
// Appointment time slot — auto-disable past dates
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('input[name="appointment_date"]');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        if (!dateInput.min) {
            dateInput.min = today;
        }
    }
});
