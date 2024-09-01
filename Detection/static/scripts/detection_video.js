document.addEventListener('DOMContentLoaded', () => {
    const videoPath = '{{ video_path }}';
    const result = '{{ result }}';

    const resultVideo = document.getElementById('resultVideo');
    resultVideo.src = videoPath;
    resultVideo.style.display = 'block';

    const resultLabel = document.getElementById('resultLabel');
    resultLabel.innerText = `Result: ${result}`;
    resultLabel.style.color = result === 'FAKE' ? 'red' : 'green';

    // Adding accessibility and loading improvements
    resultVideo.setAttribute('aria-label', 'Result video showing deepfake detection outcome');
    resultVideo.setAttribute('role', 'video');

    const loadingIndicator = document.createElement('div');
    loadingIndicator.innerText = 'Loading...';
    loadingIndicator.classList.add('loading-indicator');
    resultVideo.insertAdjacentElement('beforebegin', loadingIndicator);

    resultVideo.addEventListener('canplay', () => {
        loadingIndicator.style.display = 'none';
    });

    resultVideo.addEventListener('error', () => {
        loadingIndicator.innerText = 'Failed to load video';
        loadingIndicator.style.color = 'red';
    });
});
