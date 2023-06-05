document.getElementById('video-upload').addEventListener('submit', function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the form fields
    let title = document.getElementById('title').value;
    let description = document.getElementById('description').value;
    let video = document.getElementById('file').files[0];

    // Create a FormData instance
    let formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('video', video);

    // Send the POST request
    fetch('http://localhost:8000/crud_videos/upload_video/', {
        method: 'POST',
        body: formData,
        credentials: 'include', // セッションIDを送信するために必要
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = 'Upload successful';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
