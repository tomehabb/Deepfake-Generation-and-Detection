function openFileDialog(event) {
    const fileInput = event.currentTarget.querySelector('input[type="file"]');
    fileInput.click();
}

function handleFileChange(event) {
    const file = event.target.files[0];
    const uploadBox = document.getElementById('uploadBox');
    uploadBox.innerHTML = '';

    if (file) {
        const fileType = file.type.split('/')[0];

        if (fileType === 'image') {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            uploadBox.appendChild(img);
        } else if (fileType === 'video') {
            const video = document.createElement('video');
            video.controls = true;
            video.src = URL.createObjectURL(file);
            uploadBox.appendChild(video);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    
    uploadButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch(file.type.startsWith('image') ? '/upload_image' : '/upload_video', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(html => {
                document.body.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
});
