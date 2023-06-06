document.getElementById('video-upload').addEventListener('submit', function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the form fields
    let title = document.getElementById('title').value;
    let comment = document.getElementById('comment').value;
    let video = document.getElementById('file').files[0];

    // Create a FormData instance
    let formData = new FormData();
    formData.append('title', title);
    formData.append('comment', comment);
    formData.append('video', video);

    // Send the POST request
    fetch('http://localhost:8000/crud_videos/upload_video/', {
        method: 'POST',
        body: formData,
        credentials: 'include', // セッションIDを送信するために必要
    })
        .then(async response => {
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message);
            }
            return response.json();
        }).then(data => {
            document.getElementById('result').textContent = 'Upload successful';
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
