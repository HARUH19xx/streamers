from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import bcrypt
import psycopg2
import os
import redis
import uuid
import base64
from django.conf import settings

# 環境変数を設定する
POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

# Redisのインスタンスを作成する
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

# データベースに接続する
def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
    )

# ログインと登録の処理を設定する

#　登録処理
class RegisterView(APIView):
    """User register view."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Hash the password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )

        # Convert the hashed password to a base64 encoded string
        hashed_password_str = base64.b64encode(hashed_password).decode()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the new user into the database
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password_str))
            conn.commit()
        except psycopg2.IntegrityError:
            return Response({"error": "Username already exists."}, status=400)

        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)


# ログイン処理
class LoginView(APIView):
    """User login view."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the user
        cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            return Response({"error": "Invalid username."}, status=400)

        user_id, hashed_password = result

        # Decode hashed_password before checking
        decoded_hashed_password = base64.b64decode(hashed_password)

        # Check the password
        if not bcrypt.checkpw(password.encode('utf-8'), decoded_hashed_password):
            return Response({"error": "Invalid password."}, status=400)

        # Create a session
        r = redis.Redis(host='redis', port=6379)
        session_id = uuid.uuid4().hex
        r.set(session_id, user_id)

        response = Response({"message": "Login successful"})
        response.set_cookie('session_id', session_id, httponly=True, samesite='Lax')  # セッションIDをクッキーとしてセット

        return response
