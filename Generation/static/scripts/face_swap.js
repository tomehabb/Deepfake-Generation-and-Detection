function openFileDialogForImage(event) {
    var fileInput = event.currentTarget.querySelector('input[type="file"]')
    fileInput.click()
}

function readURL(input, imgElement) {
    if (input.files && input.files[0]) {
        var reader = new FileReader()
        reader.onload = function(e) {
            imgElement.src = e.target.result
            imgElement.classList.add('uploaded')
        }
        reader.readAsDataURL(input.files[0])
    }
}

document.querySelector('.swap-button').addEventListener('click', function() {
    var originalImage = document.getElementById('originalImage').files[0]
    var targetImage = document.getElementById('targetImage').files[0]

    if (!originalImage || !targetImage) {
        alert('Please upload both source and target images before swapping.')
        return
    }

    document.getElementById('loading').style.display = 'block'
    document.getElementById('swappedImagePreview').style.display = 'none'

    var formData = new FormData()
    formData.append('original', originalImage)
    formData.append('target', targetImage)

    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/swap', true)
    xhr.onload = function () {
        document.getElementById('loading').style.display = 'none'

        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText)
            var swappedImageBase64 = response.swapped_image
            var swappedImageElement = document.getElementById('swappedImagePreview')
            swappedImageElement.src = 'data:image/jpeg;base64,' + swappedImageBase64
            swappedImageElement.style.display = 'block'
            swappedImageElement.classList.add('uploaded')
        } else {
            alert('An error occurred while swapping the faces.')
        }
    }
    xhr.send(formData)
})

document.getElementById('originalImageContainer').addEventListener('click', function(event) {
    openFileDialogForImage(event)
})

document.getElementById('targetImageContainer').addEventListener('click', function(event) {
    openFileDialogForImage(event)
})

document.getElementById('originalImage').addEventListener('change', function() {
    readURL(this, document.getElementById('originalImageDisplay'))
})

document.getElementById('targetImage').addEventListener('change', function() {
    readURL(this, document.getElementById('targetImageDisplay'))
})
