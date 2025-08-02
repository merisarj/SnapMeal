navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        const video = document.getElementById("camera");
        video.srcObject = stream;
    })
    .catch((error) => {
    console.error("Error with camera", error);
    })

