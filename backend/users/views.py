from django.contrib.auth import authenticate
from rest_framework import authentication, permissions, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
import bcrypt
import psycopg2
import os

# 環境変数を設定する
POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')


# データベースに接続する
def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
    )

#　ログインと登録の処理を設定する
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
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            return Response({"error": "Invalid username."}, status=400)
        
        hashed_password = result[0]

        # Check the password
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return Response({"error": "Invalid password."}, status=400)
        
        # Get or create a token
        token, _ = Token.objects.get_or_create(user_id=result[0])
        return Response({"token": token.key})

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

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the new user into the database
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
        except psycopg2.IntegrityError:
            return Response({"error": "Username already exists."}, status=400)

        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
