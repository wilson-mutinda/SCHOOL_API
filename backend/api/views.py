from django.shortcuts import render, get_object_or_404

from .models import CustomUser, Role, Parent, Teacher, Student, Subject, Class, Stream, Announcement, Exams, Cat
from .serializers import (
    CustomUserSerializer, RoleSerializer, TeacherSerializer, ParentSerializer, StudentSerializer,
    SubjectSerializer, ClassSerializer, StreamSerializer, AnnouncementSerializer, ExamSerializer,
    CatSerializer
)

from rest_framework import response, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

# Function Based View to create a customUSer
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def list_create_custom_user_view(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'CustomUser Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        custom_users = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Authentication Views including tokenization
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email and not password:
        return response.Response('Both Fields are Required!', status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)

        if not user.check_password(password):
            return response.Response({'error': 'Error'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return response.Response({
            'user_id': user.id,
            "user_email": user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_admin": user.is_admin,
            "is_teacher": user.is_teacher,
            "is_parent": user.is_parent,
            "is_student": user.is_student,
        }, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return response.Response('Invalid Credentials!', status=status.HTTP_400_BAD_REQUEST)

# Class to ensure an Admin has their priviledges
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
# Create a role y an authenticated admin
@api_view(['POST', 'GET'])
@permission_classes([IsAdmin])
def list_create_role_view(request):
    if request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Role Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive, update and delete role by admin
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_role_view(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == 'GET':
        serializer = RoleSerializer(role)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = RoleSerializer(role, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        role_name = role.name
        role.delete()
        return response.Response({'message': f'{role_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create a teacher by admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_teacher_view(request):
    print("Received Data:", request.data)

    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("Saved Data:", serializer.data)
        return response.Response({'message': 'Teacher Instance Created Successfully!'}, status=status.HTTP_201_CREATED)
    print("Errors:", serializer.errors)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create a parent by admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_parent_view(request):
    print("Received Data:", request.data)

    serializer = ParentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Parent Created Successfully!'}, status=status.HTTP_201_CREATED)
    print("Errors:", serializer.errors)
    return response.Response(serializer.errors, status=status.HTTP_200_OK)

# retreive , update and delete a custom user by admin
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_custom_user_view(request, pk):
    custom_user = get_object_or_404(CustomUser, pk = pk)
    if request.method == 'GET':
        serializer = CustomUserSerializer(custom_user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = CustomUserSerializer(custom_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        custom_user_name = custom_user.username
        custom_user.delete()
        return response.Response({'message': f'{custom_user_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create a parent Class to have their priviledges
class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_parent

# view to create and student
@api_view(['POST'])
@permission_classes([IsParent])
def create_student_view(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': "Student Created Successfully!"}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create subjects by an authenticated admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_subject_view(request):
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Subject Created Successfully!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create class by an authorized admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_class_view(request):
    serializer = ClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Class Created Successfully!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create a class stream by an authorized admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_class_stream_view(request):
    serializer = StreamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Stream Created Successfully'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create an announcement by an authorized admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_announcement_view(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return response.Response({'message': 'Announcement Created Successfully!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class method to give a teacher priviledges
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher

@api_view(['POST'])
@permission_classes([IsTeacher])
def create_exam_view(request):
    data = request.data.copy()
    data['exam_teacher'] = request.user.id

    serializer = ExamSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Exam Created Successfully!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to enable a teacher create a cat
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_cat_view(request):

    serializer = CatSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'CAT Created Successfully!', 'cat_code': serializer.instance.cat_code}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
