navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        const video = document.getElementById("camera");
        video.srcObject = stream;
    })
    .catch((error) => {
    console.error("Error with camera", error);
    })

const captureBtn = document.getElementById('capture-btn');
const canvas = document.getElementById('photo');
const context = canvas.getContext('2d');
const dowloadLink = document.createElement('a');
dowloadLink.innerText = 'Dowload Photo';
document.body.appendChild(dowloadLink);

captureBtn.addEventListener('click', () => {
    const video = document.getElementById('camera');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL('image/png');

    dowloadLink.href = dataURL;
    dowloadLink.download = 'captured-photo.png';
    dowloadLink.style.display = 'block';
});




