const loginForm = document.getElementById('loginForm');
const result = document.getElementById('result');

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:8000/users/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTPエラー、ステータス: ${response.status}`);
            }
            return response.json();
        })
        .then((json) => {
            if (json.message) {
                result.innerText = 'サインアップ成功！';
                result.style.color = 'green'; // Login成功時は文字色を緑にする。
                //　ログイン画面に遷移する
                window.location.href = 'http://localhost:5500/'
            } else {
                result.innerText = 'サインアップ失敗！';
                result.style.color = 'red'; // Login失敗時は文字色を赤にする。
            }
        })
        .catch((error) => {
            result.innerText = 'エラー発生！';
            result.style.color = 'red'; // エラー発生時は文字色を赤にする。
            console.error('There has been a problem with your fetch operation:', error);
        });
});
