function openFileDialog(event) {
    var fileInput = event.currentTarget.querySelector('input[type="file"]');
    fileInput.click();
}

function openFileDialogForVideo(event) {
    var fileInput = document.getElementById('targetVideo');
    fileInput.click();
}

function readURL(input, mediaElement) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            mediaElement.src = e.target.result;
            mediaElement.classList.add('uploaded');
            if (mediaElement.tagName === 'VIDEO') {
                mediaElement.style.display = 'block';
                mediaElement.parentElement.style.border = 'none'; // Hide border once video is selected
                mediaElement.load(); // Ensure the video is loaded
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

document.querySelector('.swap-button').addEventListener('click', function() {
    var originalImage = document.getElementById('originalImage').files[0];
    var targetVideo = document.getElementById('targetVideo').files[0];

    if (!originalImage || !targetVideo) {
        alert('Please upload an image and a video before swapping.');
        return;
    }

    document.getElementById('loading').style.display = 'block';
    document.getElementById('swappedVideoPreview').style.display = 'none';

    var formData = new FormData();
    formData.append('original', originalImage);
    formData.append('target', targetVideo);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/swap_video', true);
    xhr.onload = function () {
        document.getElementById('loading').style.display = 'none';

        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var swappedVideoUrl = response.swapped_video;
            var swappedVideoElement = document.getElementById('swappedVideoPreview');
            swappedVideoElement.src = swappedVideoUrl;
            swappedVideoElement.style.display = 'block';
            swappedVideoElement.load(); // Ensure the video is loaded
        } else {
            alert('An error occurred while swapping the faces.');
        }
    };
    xhr.send(formData);
});
