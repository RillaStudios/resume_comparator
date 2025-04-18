from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from api.models.user import User
from api.serializers.user_serializer import UserSerializer
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import render

"""
User Views

This view is used to register, login, logout, protected route, get user details, update, change pass and delete user.

Author: Michael Tamatey
Date: 2025-03-05
"""

# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


"""
User Register method

Author: Michael Tamatey
Date: 2025-03-05
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # Extract email and username from the request data
    email = request.data.get('email')
    username = request.data.get('username')

    # Check if the email or username already exists
    if User.objects.filter(email=email).exists():
        return Response({
            "message": "Email is already registered."
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({
            "message": "Username is already taken."
        }, status=status.HTTP_400_BAD_REQUEST)

    # If no duplicates, proceed with serialization and saving the user
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "User registered successfully",
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
User Login method

Author: Michael Tamatey
Date: 2025-03-05
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })



"""
User Logout method (Client-side should delete token)

Author: Michael Tamatey
Date: 2025-03-05
"""
# 
@api_view(['POST'])
def logout(request):
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)



"""
Protected Route method 

Author: Michael Tamatey
Date: 2025-03-05
""" 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}! This is a protected route."})


"""
Change Password method 

Author: Michael Tamatey
Date: 2025-03-05
"""  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user
    username = request.data.get('username')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not username or not old_password or not new_password:
        return Response({"error": "All fields (username, old password, new password) are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the user matches the username in the request
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(old_password):
        return Response(
            {"error": "Old password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


"""
Get User method

Author: Michael Tamatey
Date: 2025-03-05
"""
# View Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)



"""
Update Profile method

Author: Michael Tamatey
Date: 2025-03-05
"""
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates

    if serializer.is_valid():
        if "password" in request.data:  # If user updates password, hash it
            user.set_password(request.data["password"])
        serializer.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Delete User Account method

Author: Michael Tamatey
Date: 2025-03-05
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    password = request.data.get("password")

    if not password:
        return Response({"error": "Password is required to delete account"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)





"""
Verify and send email method

Author: Michael Tamatey
Date: 2025-04-07
"""
@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message": "If the email is registered, you will receive a reset link."}, status=200)

    # Generate the unique reset link
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"{request.scheme}://{request.get_host()}/api/reset/{uid}/{token}/"
    message = render_to_string('register/password_reset_email.html', {'reset_link': reset_link, 'user': user})
    
    # Send the reset link via email
    send_mail(
        'Password Reset Request',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return JsonResponse({"message": "If the email is registered, you will receive a reset link soon."}, status=200)

"""
Reset password method

Author: Michael Tamatey
Date: 2025-04-07
"""
@api_view(['GET', 'POST'])
def confirm_password(request, uidb64, token):
    try:
        # Decode the uid and retrieve the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return render(request, 'register/reset_password.html', {'error': 'Invalid reset link.'})

    # Check if the token is valid
    if not default_token_generator.check_token(user, token):
        return render(request, 'register/reset_password.html', {'error': 'The reset link is invalid or has expired.'})

    if request.method == 'POST':
        # Handle form submission to reset password
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register/reset_password.html', {'message': 'Your password has been reset successfully. Go to the login page.'})
    else:
        # Display the form if it's a GET request
        form = SetPasswordForm(user)

    return render(request, 'register/reset_password.html', {'form': form})
