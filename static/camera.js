document.addEventListener("DOMContentLoaded", () => {
    navigator.mediaDevices.getUserMedia({video: true})
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

    captureBtn.addEventListener('click', () => {
        const video = document.getElementById('camera');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataURL = canvas.toDataURL('image/jpeg', 0.9);
        function dataURLBlob(dataUrl) {
            const arr = dataUrl.split(',');
            const mime = arr[0].match(/:(.*?);/)[1];
            const bstr = atob(arr[1]);
            let n = bstr.length;
            const u8arr = new Uint8Array(n);
            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new Blob([u8arr], {type: mime});
        }

        const blob = dataURLBlob(dataURL);

        const formData = new FormData();
        formData.append('file', blob, 'captured-image.jpg');

        fetch('/Upload-Image', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(result => {
                console.log('AI API Response:', result);
                document.getElementById("result").textContent = result.output || JSON.stringify(result);
            })
            .catch(error => {
                console.error('Error sending image to AI API', error);
            })

        const dowloadLink = document.createElement('a');
        dowloadLink.href = dataURL;
        dowloadLink.download = 'captured-photo.png';
        dowloadLink.style.display = 'block';
        dowloadLink.click();
    });
})




