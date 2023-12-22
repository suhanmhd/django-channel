# from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
# from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# from .serializers import *
from dbuserapp.models import User
# from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer  # Import your UserSerializer from the correct location
from rest_framework.decorators import permission_classes




@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate unique username and email
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user with hashed password
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            print("User created successfully")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Use DRF Token or JWT for token generation
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Use DRF Serializer for user serialization
            serialized_data = UserSerializer(user)

            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
                'message': 'User logged in successfully',
                'userDetails': serialized_data.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_document(request):
#     if request.method == 'POST':
#         document_title = request.data.get('documentTitle')
#         document_content = request.data.get('documentContent')
#         user_id = request.data.get('id')

#         try:
#             user_obj = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Create a new document for the user
#         document_obj = Documents.objects.create(user=user_obj, title=document_title, content=document_content)

#         return Response({'message': 'Document created successfully'}, status=status.HTTP_201_CREATED)

#     return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([IsAuthenticated])
# class GetDocuments(APIView):
#     def post(self, request):
#         user_id = request.data.get('id')

#         try:
#             user_obj = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Create a new document for the user
#         document_obj = Documents.objects.filter(user=user_obj)

#         # Serialize the document object
#         serializer = DocumentSerializer(document_obj, many=True)

#         return Response({'message': 'Document obtained successfully', 'documents':serializer.data}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def delete_document(request):
#     if request.method == 'POST':
        
#         try:
#             doc_id = request.data.get('id')
#             object_id = ObjectId(doc_id)
#             documentobj = Documents.objects.get(_id=object_id)

#             documentobj.delete()

#         except User.DoesNotExist:
#             return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

#         return Response({'message': 'Document deleted successfully'}, status=status.HTTP_201_CREATED)

#     return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        # Log out the user
        logout(request)
        return Response({'message': 'User loggedOut successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token_refresh_view(request):
    """
    A view to refresh an access token using a refresh token.
    """
    serializer = TokenRefreshView.get_serializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    refresh = serializer.validated_data.get('refresh')
    access = RefreshToken(refresh).access_token

    # Return the new access token
    return Response({'access_token': str(access)}, status=status.HTTP_200_OK)
