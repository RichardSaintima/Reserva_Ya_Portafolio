document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message_input');
    const imageInput = document.getElementById('image_input');
    const imageButton = document.getElementById('image_button');
    const previewContainer = document.createElement('div');
    previewContainer.classList.add('preview_container');
    const mostrarfile = document.getElementById('mostrarfile');

    imageButton.addEventListener('click', function() {
        imageInput.click();
    });

    imageInput.addEventListener('change', function() {
        const file = imageInput.files[0];
        if (file) {
            const extension = file.name.split('.').pop().toLowerCase();
            const icon = document.createElement('i');
            const fileName = document.createElement('p');
            icon.classList.add('file_icon');
            fileName.classList.add('file_name');
    
            if (extension === 'pdf') {
                icon.classList.add('fa', 'fa-file-pdf');
            } else if (extension === 'png' || extension === 'jpg' || extension === 'jpeg') {
                icon.classList.add('fa', 'fa-file-image');
            } else {
                icon.classList.add('fa', 'fa-file');
            }
    
            fileName.innerText = file.name;
    
            mostrarfile.innerHTML = '';
            mostrarfile.appendChild(icon);
            mostrarfile.appendChild(fileName);
            mostrarfile.classList.add('mostrarfile');
        } else {
            mostrarfile.innerHTML = '';

        }
    });    
    
    messageInput.addEventListener('input', function() {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    });
});
