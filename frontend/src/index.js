fetch('http://localhost:8000/crud_videos/hello/')
    .then(response => response.json())
    .then(data => console.log(data));

document.getElementById('login-form').addEventListener('submit', function (event) {
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
        credentials: 'include',
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Login successful') {
                // メッセージが 'Login successful' であれば、ログイン成功と判断
                document.getElementById('result').textContent = 'Login successful';
                // ダッシュボードへリダイレクト
                window.location.href = '/dashboard.html';
            } else {
                // そうでない場合、ログイン失敗と判断
                document.getElementById('result').textContent = 'Login failed';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});