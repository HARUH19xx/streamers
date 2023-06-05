import os
import boto3
import redis
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from pathlib import Path
from datetime import datetime
from django.db import connection

# AWS S3設定
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

s3_client = boto3.client('s3', region_name=AWS_REGION, 
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

#　認証処理
class IsAuthenticatedWithRedis(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get('session_id')
        if session_id is None:
            return False

        user_id = redis_instance.get(session_id)
        if user_id is None:
            return False

        request.user_id = user_id  # Add user_id to request object so we can use it later

        return True


# 「こんにちは」と返すだけのAPI
@api_view(['GET'])
def hello(request):
    return Response({'message': 'こんにちは'}, status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticatedWithRedis])
def upload_video(request):
    try:
        if 'video' in request.FILES:
            video = request.FILES['video']
            comment = request.data.get('comment', '')

            # ローカルへ一時保存
            local_path = default_storage.save(f'tmp/video/{datetime.now().strftime("%Y%m%d%H%M%S")}_{video.name}', ContentFile(video.read()))
            absolute_local_path = os.path.join(settings.MEDIA_ROOT, local_path)
            
            # S3へアップロード
            with open(absolute_local_path, 'rb') as data:
                s3_client.upload_fileobj(data, AWS_S3_BUCKET_NAME, f'uploads/{Path(local_path).name}')

            # データベースにコメントと動画のURLを保存
            video_url = f'https://{AWS_S3_BUCKET_NAME}.s3-{AWS_REGION}.amazonaws.com/uploads/{Path(local_path).name}'
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO posts (user_id, video_url, comment) VALUES (%s, %s, %s)', [request.user_id, video_url, comment])

            # ローカルの動画ファイルを削除
            os.remove(absolute_local_path)

            return Response({'success': True, 'message': '動画をアップロードしました。', 'videoUrl': video_url}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': '動画ファイルが必要です。'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'success': False, 'message': f'サーバーエラーが発生しました。{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
