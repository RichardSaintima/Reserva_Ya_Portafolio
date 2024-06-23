document.addEventListener('DOMContentLoaded', function() {
    const deleteAccountButton = document.getElementById('delete_account');
    const deleteModal = document.getElementById('delete_modal');
    const closeButton = document.querySelector('.close_button');
    const cancelButton = document.querySelector('.cancel_button');

    deleteAccountButton.addEventListener('click', function() {
        deleteModal.style.display = 'block';
    });

    closeButton.addEventListener('click', function() {
        deleteModal.style.display = 'none';
    });

    cancelButton.addEventListener('click', function() {
        deleteModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == deleteModal) {
            deleteModal.style.display = 'none';
        }
    });
});
