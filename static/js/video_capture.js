let imageDataUrl;
const content = document.querySelector('#video-stream');

const videoElement = document.createElement('video');
const canvas = document.createElement('canvas');
content.appendChild(canvas);
let canvasContext = canvas.getContext('2d', { willReadFrequently: true });

function processFrame() {
    canvasContext.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    const frameData = canvasContext.getImageData(0, 0, canvas.width, canvas.height, );
    imageDataUrl = canvas.toDataURL('image/jpeg');

    requestAnimationFrame(processFrame)
}

navigator.mediaDevices.getUserMedia({video: true})
    .then(stream => {
        videoElement.srcObject = stream;
        videoElement.play();
        requestAnimationFrame(processFrame)
    });

async function capture_frame(url, username, imageDataURL) {
    console.log(url)
    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({image: imageDataURL, name: username})
    })
    .then(response => {
        response.json()
    })
    .then(data => {
        // Process the response from the server
        console.log('Server response:', data);
    });
}

const registerFace = document.querySelector('#register_face_data');
const loginFace = document.querySelector('#check_face_data');

if (registerFace === null) {
    loginFace.addEventListener('click', async () => {
        console.log('Im running.')
        await login_face_data(loginFace.dataset.username)
    });
} else {
    registerFace.addEventListener('click', async () => {
        await register_face_data(registerFace.dataset.username)
    });
}
async function register_face_data(username) {
    await capture_frame(`/save_face_data`, username, imageDataUrl);
    window.location.href = '/login'
}
async function login_face_data(username) {
    console.log('Im running.')
    await capture_frame(`/check_face_data`, username, imageDataUrl);
    window.location.href = '/'
}





