function updateFileName() {
    const fileInput = document.getElementById('fileInput');
    const fileLabel = document.getElementById('fileLabel');

    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;

        if (!document.getElementById('removeFileIcon')) {
            const removeIcon = document.createElement('span');
            removeIcon.id = 'removeFileIcon';
            removeIcon.innerHTML = '&times;';
            removeIcon.style.cursor = 'pointer';
            removeIcon.style.marginLeft = '5px';
            removeIcon.addEventListener('click', removeFile);
            fileLabel.appendChild(removeIcon);
        }
    } else {
        fileLabel.textContent = 'Browse...';

        const removeIcon = document.getElementById('removeFileIcon');
        if (removeIcon) {
            removeIcon.remove();
        }
    }
}

function removeFile() {
    const fileInput = document.getElementById('fileInput');
    fileInput.value = '';
    updateFileName(); 
}
