from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

import pandas as pd
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from user_app.api.serializer import (
    RegistrationSerializer
)


@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Successfully registered a new user.'
            data['username'] = account.username
            data['email'] = account.email
            
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            data = serializer.errors
        return Response(data)
    
    
@csrf_exempt
def upload_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        file_name = default_storage.save(excel_file, ContentFile(excel_file.read()))
        file_path = default_storage.path(file_name)
        
        try:
            df = pd.read_excel(file_path)
            
            # Check for repeated emails in the uploaded Excel file
            if df['email'].duplicated().any() or df['username'].duplicated().any():
                default_storage.delete(file_name)
                return JsonResponse({'error': 'Duplicate emails (or) usernames found in the uploaded file'}, status=400)
            
            # Check for emails that already exist in the database
            existing_emails = User.objects.filter(email__in=df['email']).values_list('email', flat=True)
            existing_usernames = User.objects.filter(username__in=df['username']).values_list('username', flat=True)
            if existing_emails or existing_usernames:
                error_message = ''
                if existing_emails:
                    error_message += f'These emails already exist in the database: {", ".join(existing_emails)}. '
                if existing_usernames:
                    error_message += f'These usernames already exist in the database: {", ".join(existing_usernames)}.'
                
                default_storage.delete(file_name)
                return JsonResponse({'error': error_message.strip()}, status=400)
            
            
            for index, row in df.iterrows():
                User.objects.create_user(
                    username=row['username'],
                    password=row['password'],
                    email=row['email']
                )
            # Delete the file after processing
            default_storage.delete(file_name)
            return JsonResponse({'message': 'Users created successfully'}, status=201)
        except Exception:
            # Delete the file if an error occurred
            default_storage.delete(file_name)
            return JsonResponse({'error': str(Exception)}, status=400)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)