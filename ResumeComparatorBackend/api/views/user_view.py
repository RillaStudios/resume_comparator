from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from api.models.user import User
from api.serializers.user_serializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate


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
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    # If the old password is correct, set the new password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


"""
Change Password method

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

    if not user.check_password(password):  # Verify password
        return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)