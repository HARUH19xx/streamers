fetch('http://localhost:8000/crud_videos/hello/')
    .then(response => response.json())
    .then(data => console.log(data));

document.getElementById('login-form').addEventListener('submit', function(event) {
    // フォームのデフォルトの送信動作を停止
    event.preventDefault();

    // フォームからユーザーネームとパスワードを取得
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // サーバーにPOSTリクエストを送信
    fetch('http://localhost:8000/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // レスポンスにトークンが含まれている場合、ログイン成功
            document.getElementById('result').textContent = 'Login successful';
        } else {
            // レスポンスにトークンが含まれていない場合、ログイン失敗
            document.getElementById('result').textContent = 'Login failed';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
