from django.shortcuts import render, get_object_or_404
import requests

from .models import (
    CustomUser, Role, Parent, Teacher, Student, 
    Subject, Class, Stream, Announcement, CatGrading, 
    Cats, Exam, ExamGrading, CatAndExam, StreamClassSubjects,
    CatAndExamGrading, FinalGrade, ReportForm, Term, CustomUserAdmin
)
from .serializers import (
    CustomUserSerializer, RoleSerializer, TeacherSerializer, ParentSerializer, StudentSerializer,
    SubjectSerializer, ClassSerializer, StreamSerializer, AnnouncementSerializer, CatGradingSerializer, 
    CatSerializer, ExamSerializer, ExamGradingSerializer, CatAndExamSerailizer, StreamClassSubjectSerializer,
    CatAndExamGradingSerializer, FinalGradeSerializer, ReportFormSerializer, TermSerializer, CustomUserAdminSerializer
)

from rest_framework import response, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.response import Response
from .zoom import create_zoom_meeting
from datetime import datetime

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
        
        parent_profile_url = None
        teacher_profile_url = None
        role_code = None  # will hold parent_code, teacher_code, or student_code

        if user.is_teacher:
            try:
                teacher_profile = user.teachers
                if teacher_profile.profile_picture:
                    teacher_profile_url = request.build_absolute_uri(teacher_profile.profile_picture.url)
                role_code = teacher_profile.teacher_code
            except Teacher.DoesNotExist:
                pass

        if user.is_parent:
            try:
                parent_profile = user.parents
                if parent_profile.profile_picture:
                    parent_profile_url = request.build_absolute_uri(parent_profile.profile_picture.url)
                role_code = parent_profile.parent_code
            except Parent.DoesNotExist:
                pass

        if user.is_student:
            try:
                student_profile = user.students
                role_code = student_profile.student_code
            except Student.DoesNotExist:
                pass

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return response.Response({
            'user_id': user.id,
            "user_email": user.email,
            'first_letter': user.email[0].upper(),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_admin": user.is_admin,
            "is_teacher": user.is_teacher,
            "is_parent": user.is_parent,
            "is_student": user.is_student,
            'teacher_profile_picture': teacher_profile_url,
            'parent_profile_picture': parent_profile_url,
            'role_code': role_code  # 👈 This is the important part
        }, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return response.Response('Invalid Credentials!', status=status.HTTP_400_BAD_REQUEST)


# Class to ensure an Admin has their priviledges
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    

# create a zoom meeting
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def create_meeting(request):
    try:
        topic = request.data.get('topic', f"Consultation with {request.user.username}")
        duration = int(request.data.get('duration', 30))

        # Get and validate date/time
        start_date = request.data.get('start_date')
        start_time = request.data.get('start_time')

        if not start_date or not start_time:
            return response.Response({'error': 'start_date and start_time are required'}, status=400)

        try:
            # Combine date and time into a datetime object and convert to ISO format in UTC
            dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
            start_time_str = dt.isoformat() + "Z"  # Add 'Z' to mark UTC
        except ValueError:
            return response.Response({'error': 'Invalid date or time format'}, status=400)

        # Create the meeting
        meeting_data = create_zoom_meeting(topic, duration, start_time_str)

        if 'error' in meeting_data:
            return response.Response(
                {'error': meeting_data['error']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response.Response({
            'join_url': meeting_data.get('join_url'),
            'meeting_id': meeting_data.get('id'),
            'password': meeting_data.get('password')
        })

    except Exception as e:
        return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# function class to combine both admin and teacher to have same priviledges
class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_teacher)

# function view to enable a superadmin create other admins
@api_view(['POST', 'GET'])
@permission_classes([permissions.AllowAny])
def create_admin_view(request):
    if request.method == 'POST':
        serializer = CustomUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': "Admin Created Successfully!"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        admins = CustomUserAdmin.objects.all()
        serializer = CustomUserAdminSerializer(admins, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# superadmin function view to retreive and update an admin
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_admin_view(request, pk):
    try:
        admin = CustomUserAdmin.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = CustomUserAdminSerializer(admin)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CustomUserAdminSerializer(admin, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            admin_name = admin.username
            admin.delete()
            return response.Response({'message': f'{admin_name} deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUserAdmin.DoesNotExist:
        return response.Response({'message': 'Admin does not exist!'}, status=status.HTTP_204_NO_CONTENT)
    
# Create a role by an authenticated admin
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

# create a term by admin
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_term_view(request):
    serializer = TermSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Successfully Created!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin retreive and update term
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_term_view(request, name):
    try:
        normalized_name = name.lower()
        term = Term.objects.get(name__iexact=normalized_name)

        if request.method == 'GET':
            serializer = TermSerializer(term)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = TermSerializer(term, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            term.delete()
            return response.Response({'message': 'Term Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Term.DoesNotExist:
        return response.Response({'message': 'Term Does Not Exist!'})

# Create a teacher by admin
@api_view(['POST', 'GET'])
@permission_classes([permissions.AllowAny])
def create_teacher_view(request):
    if request.method == 'POST':
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("Saved Data:", serializer.data)
            return response.Response({'message': 'Teacher Instance Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create a parent by admin
@api_view(['POST', 'GET'])
@permission_classes([permissions.AllowAny])
def create_parent_view(request):
    if request.method == 'POST':
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Parent Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_OK)

# retreive , update and delete a custom user by admin using role_id
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_custom_user_view(request, role_id):
    custom_user = get_object_or_404(CustomUser, role_id=role_id)
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
    
# view to create a student by a admin and a teacher
class IsParentAdminTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_teacher or request.user.is_parent)
    
# view to create a student by a admin and a teacher
class IsParentAdminTeacherStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_teacher or request.user.is_parent or request.user.is_student)

# view to create and student
@api_view(['POST', 'GET'])
@permission_classes([IsParentAdminTeacher])
def create_student_view(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': "Student Created Successfully!"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create subjects by an authenticated admin
@api_view(['POST', 'GET'])
@permission_classes([IsAdmin])
def create_subject_view(request):
    if request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Subject Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# subject info
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_subject_view(request, pk):
    try:
        subject = Subject.objects.get(id=pk)
        
        if request.method == 'GET':
            serializer = SubjectSerializer(subject)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = SubjectSerializer(subject, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            subject_name = subject.name
            subject.delete()
            return response.Response({'message': f'{subject_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Subject.DoesNotExist:
        return response.Response({'message': f'{subject} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# create class by an authorized admin
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_class_view(request):
    if request.method == 'POST':
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Class Created Successfully!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete class
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_class_view(request, pk):
    try:
        class_name = Class.objects.get(id=pk)

        if request.method == 'GET':
            serializer = ClassSerializer(class_name)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ClassSerializer(class_name, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response({'message': 'Class Created Successfully'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            name = class_name.name
            class_name.delete()
            return response.Response({'message': f'{name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Class.DoesNotExist:
        return response.Response({'message': f'{class_name} does not exist!'})

# create a class stream by an authorized admin
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_class_stream_view(request):
    if request.method == 'POST':
        serializer = StreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Stream Created Successfully'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        streams = Stream.objects.all()
        serializer = StreamSerializer(streams, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete stream
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_stream_view(request, pk):
    try:
        stream = Stream.objects.get(id=pk)

        if request.method == 'GET':
            serializer = StreamSerializer(stream)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = StreamSerializer(stream, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            stream_name = stream.name
            stream.delete()
            return response.Response({'message': f'{stream_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Stream.DoesNotExist:
        return response.Response({'message': f'{stream} does not exist!'}, status=status.HTTP_404_NOT_FOUND)

# create an announcement by an authorized admin
@api_view(['POST'])
@permission_classes([IsAdminOrTeacher])
def create_announcement_admin_view(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return response.Response({'message': 'Announcement Created Successfully!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive the number of announcements
@api_view(['GET'])
@permission_classes([IsAdmin])
def retreive_number_of_announcements_view(request):
    announcements = Announcement.objects.all()
    total = announcements.count()
    return response.Response({
        'message': 'Successful',
        'Total Announcements': total
    }, status=status.HTTP_200_OK)

# class to ensure announcements teachers
class IsAdminTeacherAnnouncement(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
# retreive teacher targeted announce,ents
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_teacher_targeted_announcements_view(request):
    announcements = Announcement.objects.filter(target_teachers=True)
    total = announcements.count()
    serailizer = AnnouncementSerializer(announcements, many=True)
    # fetch the title
    titles = []
    for announcement in serailizer.data:
        titles.append(announcement['title'])

    # fetch the description
    descriptions = []
    for announcement in serailizer.data:
        descriptions.append(announcement.get('description'))

    # fetch the date
    date_created = []
    for announcement in serailizer.data:
        date_created.append(announcement.get('date_created'))
    return response.Response({
        'message': 'Successful',
        'Total': total,
        'Announcements': serailizer.data
    }, status=status.HTTP_200_OK)

# retreive the student targeted announcements
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_student_targeted_announcements_view(request):
    announcements = Announcement.objects.filter(target_students=True)
    total = announcements.count()

    serailizer = AnnouncementSerializer(announcements, many=True)
    return response.Response({
        'message': 'Successful',
        'Total': total,
        'Announcements': serailizer.data
    }, status=status.HTTP_200_OK)

# retreive parent targeted announcements
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_parent_targeted_announcements_view(requeest):
    announcements = Announcement.objects.filter(target_parents=True)
    total = announcements.count()
    serializer = AnnouncementSerializer(announcements, many=True)

    return response.Response({
        'message': 'Successful',
        'Total': total,
        'Announcements': serializer.data
    }, status=status.HTTP_200_OK)

# admin targeted announcements
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_admin_targeted_announcements_view(request):
    announcements = Announcement.objects.filter(target_admins=True)
    total = announcements.count()
    serializer = AnnouncementSerializer(announcements, many=True)

    return response.Response({
        'message': 'Successful',
        'Total': total,
        'Announcements': serializer.data
    }, status=status.HTTP_200_OK)

# class method to give a teacher priviledges
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher
    
# function to create a cat by an authorized teacher
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_cat_view(request):
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Cat Created!'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        cats = Cats.objects.all()
        serializer = CatSerializer(cats, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin to reteive and update a cat
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_cat_admin_view(request, pk):
    try:
        cat = Cats.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = CatSerializer(cat)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CatSerializer(cat, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            cat.delete()
            return response.Response({'message': 'Cat Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Cats.DoesNotExist:
        return response.Response({'message': f'Cat ({cat}) does not exist!'}, status=status.HTTP_404_NOT_FOUND)
    
# admin to retreive a report form using student code and update or delete
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_reportform_admin_view(request, student_code):
    
    try:
        reportform = ReportForm.objects.get(student_code=student_code)

        if request.method == 'GET':
            serializer = ReportFormSerializer(reportform)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ReportFormSerializer(reportform, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            reportform.delete()
            return response.Response({'message': f'ReportForm ({reportform}) Deleted!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ReportForm.DoesNotExist:
        return response.Response({'message': f'Student Report Form for ({reportform}) Not Found!'}, status=status.HTTP_404_NOT_FOUND)

# function to grade a cat
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_cat_grade_view(request):
    if request.method == 'POST':
        serializer = CatGradingSerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Cat Graded successfully!'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        cat_grades = CatGrading.objects.all()
        serializer = CatGradingSerializer(cat_grades, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete cat grade
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_cat_grade_view(request, pk):
    try:
        cat_grade = CatGrading.objects.get(id=pk)

        if request.method == 'GET':
            serializer = CatGradingSerializer(cat_grade)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CatGradingSerializer(cat_grade, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            cat_grade_name = cat_grade.cat_name
            cat_grade.delete()
            return response.Response({'message': f'{cat_grade_name} deleted successfuly'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CatGrading.DoesNotExist:
        return response.Response({'message': f'{cat_grade} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# permit a logged in teacher and admin to create view exams
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_retreive_exam_view(request):
    if request.method == 'POST':
        serializer = ExamSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Exam Created'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# permit a teacher to grade a student exam
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_exam_grade_view(request):
    if request.method == 'POST':
        serializer = ExamGradingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Exam Graded'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        exam_grades = ExamGrading.objects.all()
        serializer = ExamGradingSerializer(exam_grades, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete exam grade
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_exam_grade_view(request, pk):
    try:
        exam_grade = ExamGrading.objects.get(id=pk)

        if request.method == 'GET':
            serializer = ExamGradingSerializer(exam_grade)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ExamGradingSerializer(exam_grade, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            exam_grade_name = exam_grade.exam_name
            exam_grade.delete()
            return response.Response({'message': f'{exam_grade_name} deleted successfuly'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ExamGrading.DoesNotExist:
        return response.Response({'message': f'{exam_grade} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function view to create a cat and exam by an authorized teacher
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_exam_and_cat_view(request):
    if request.method == 'POST':
        serializer = CatAndExamSerailizer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        exams_and_cats = CatAndExam.objects.all()
        serializer = CatAndExamSerailizer(exams_and_cats, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete cat and exam 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_exam_and_cat_view(request, pk):
    try:
        exam_and_cat = CatAndExam.objects.get(id=pk)

        if request.method == 'GET':
            serializer = CatAndExamSerailizer(exam_and_cat)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CatAndExamSerailizer(exam_and_cat, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            exam_and_cat.delete()
            return response.Response({'message': 'Instance Deleted Successfull'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CatAndExam.DoesNotExist:
        return response.Response({'message': f'{exam_and_cat} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function to generate a student with class and stream
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_class_stream_subject_view(request):
    if request.method == 'POST':
        serializer = StreamClassSubjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        stream_class_subjects = StreamClassSubjects.objects.all()
        serializer = StreamClassSubjectSerializer(stream_class_subjects, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retreive update delete cat and exam 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_class_stream_subject_view(request, pk):
    try:
        class_stream_subject = StreamClassSubjects.objects.get(id=pk)

        if request.method == 'GET':
            serializer = StreamClassSubjectSerializer(class_stream_subject)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = StreamClassSubjectSerializer(class_stream_subject, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            class_stream_subject.delete()
            return response.Response({'message': 'Instance Deleted Successfull'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CatAndExam.DoesNotExist:
        return response.Response({'message': f'{class_stream_subject} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function view to calculate the grand total of subject cat and exam
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_overall_subject_grade_view(request):
    if request.method == 'POST':
        serializer = CatAndExamGradingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            subject_grade = CatAndExamGrading.objects.all()
            serializer = CatAndExamGradingSerializer(subject_grade, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# retreive update delete catandexam grade
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_cat_and_exam_grade_view(request, pk):
    try:
        cat_and_exam_grade = CatAndExamGrading.objects.get(id=pk)

        if request.method == 'GET':
            serializer = CatAndExamGradingSerializer(cat_and_exam_grade)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CatAndExamGradingSerializer(cat_and_exam_grade, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            grading_name = cat_and_exam_grade.subject_grade
            cat_and_exam_grade.delete()
            return response.Response({'message': f'{grading_name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CatAndExamGrading.DoesNotExist:
        return response.Response({'message': f'{cat_and_exam_grade} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function to get the final grade
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_final_grade_view(request):
    if request.method == 'POST':
        serializer = FinalGradeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            subject_grade = FinalGrade.objects.all()
            serializer = FinalGradeSerializer(subject_grade, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# retreive update delete final grade
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_final_grade_view(request, pk):
    try:
        final_grade = FinalGrade.objects.get(id=pk)

        if request.method == 'GET':
            serializer = FinalGradeSerializer(final_grade)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = FinalGradeSerializer(final_grade, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            grade = final_grade.final_grade
            final_grade.delete()
            return response.Response({'message': f'{grade} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except FinalGrade.DoesNotExist:
        return response.Response({'message': f'{final_grade} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function to generate a report form 
@api_view(['POST', 'GET'])
@permission_classes([IsAdminOrTeacher])
def create_report_form_view(request):
    if request.method == 'POST':
        serializer = ReportFormSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            report_forms = ReportForm.objects.all()
            serializer = ReportFormSerializer(report_forms, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# retreive update delete report form
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_report_form_view(request, pk):
    try:
        report_form = ReportForm.objects.get(id=pk)

        if request.method == 'GET':
            serializer = ReportFormSerializer(report_form)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ReportFormSerializer(report_form, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            report = report_form.total_subjects
            report_form.delete()
            return response.Response({'message': f'{report} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ReportForm.DoesNotExist:
        return response.Response({'message': f'{report_form} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# function to calcukate the number of teachers
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def get_the_number_of_registered_teachers(request):
    teachers = Teacher.objects.all()
    total = teachers.count()

    return response.Response({
        'message': f"Successful",
        'Total': total
    }, status=status.HTTP_200_OK)

# admin function to fetch all teachers
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def fetch_all_teachers_view(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True, context={'request': request})
    return response.Response(serializer.data, status=status.HTTP_200_OK)

# admin function to fwtch all students
@api_view(['GET'])
@permission_classes([IsParentAdminTeacherStudent])
def fetch_all_students_view(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True, context={'request': request})
    return response.Response(serializer.data, status=status.HTTP_200_OK)

# admin function to fetch all parents
@api_view(['GET'])
@permission_classes([IsParentAdminTeacher])
def fetch_all_parents_view(request):
    parents = Parent.objects.all()
    serializer = ParentSerializer(parents, many=True, context={'request': request})
    return response.Response(serializer.data, status=status.HTTP_200_OK)

# function to ensure admin can view and change teacher details
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_destoy_teacher_info_view(request, pk):

    try:
        teacher = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        return response.Response({'message': 'Teacher Not Available!'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TeacherSerializer(teacher)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        teacher.delete()
        return response.Response({'message': 'Teacher deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to ensure admin can view and update student dtails
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_update_delete_student_info_view(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
            
        elif request.method == 'PATCH':
            # Make a mutable copy of request data
            request_data = request.data.copy()
            
            # If user data is included, ensure we keep the existing username and email
            if 'user' in request_data:
                request_data['user']['username'] = student.user.username
                request_data['user']['email'] = student.user.email
                
            serializer = StudentSerializer(
                student, 
                data=request_data, 
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            student.delete()
            return response.Response({'message': 'Student Deleted'}, status=status.HTTP_204_NO_CONTENT)
            
    except Student.DoesNotExist:
        return response.Response({'message': 'Student not found!'}, status=status.HTTP_404_NOT_FOUND)

# function to ensure  an admin can view and update parent details
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsParentAdminTeacherStudent])
def retreive_update_delete_parent_info_view(request, pk):
    try:
        parent = Parent.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = ParentSerializer(parent)
            return response.Response(serializer.data)
            
        elif request.method == 'PATCH':
            # Handle multipart form data
            data = request.data.dict() if hasattr(request.data, 'dict') else request.data
            serializer = ParentSerializer(parent, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)  # Return the updated data, not errors
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            parent.delete()
            return response.Response({'message': 'Parent Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
            
    except Parent.DoesNotExist:
        return response.Response({'message': 'Parent Does not Exist!'}, status=status.HTTP_404_NOT_FOUND)
    
# function to allow an and and admin retreive and update exam details
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_exam_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = ExamSerializer(exam)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            serializer = ExamSerializer(exam, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            exam_name = exam.exam_name
            exam.delete()
            return response.Response({'message': f'{exam_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exam.DoesNotExist:
        return response.Response({'message': "Exam Does Not Exist!"}, status=status.HTTP_404_NOT_FOUND)
    
# function to ensure admin can retreive and update a class
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_class_view(request, pk):

    try:
        name = Class.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = ClassSerializer(name)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            serializer = ClassSerializer(name, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            name.delete()
            return response.Response({'message': 'Class Deleted!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Class.DoesNotExist:
        return response.Response({'message': 'Class Does Not Exist!'}, status=status.HTTP_204_NO_CONTENT)
    
# function for an admin to view the available streams
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_stream_info_view(request, pk):

    try:
        stream = Stream.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = StreamSerializer(stream)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = StreamSerializer(stream, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            stream.delete()
            return response.Response({'message': 'Stream Deleted!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Stream.DoesNotExist:
        return response.Response({'message': 'Stream Does Not Exist!'}, status=status.HTTP_204_NO_CONTENT)
    
# function to ensure an admin and teacher can be able to view student reaults
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_report_form_admin_teacher_view(request, student_code):

    try:
        student = ReportForm.objects.get(student_code=student_code)

        if request.method == 'GET':
            serializer = ReportFormSerializer(student)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            serializer = ReportFormSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            student.delete()
            return response.Response({'message': 'Student Results Deleted!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ReportForm.DoesNotExist:
        return response.Response({'message': 'Student Not Graded!'}, status=status.HTTP_404_NOT_FOUND)
    
# class method to give the parent priviledges to view students results and progress
class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_parent
    
# give the parent priviledges to view sudent results
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsParent])
def retreive_update_delete_report_form_parent_view(request, student_code):
    try:
        student = ReportForm.objects.get(student_code=student_code)

        if request.method == 'GET':
            serializer = ReportFormSerializer(student)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ReportFormSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            student.delete()
            return response.Response({'message': 'Student Report Deleted!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ReportForm.DoesNotExist:
        return response.Response({'message': 'Student Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)
    
# function to enable admin view the number of custom users
@api_view(['GET'])
@permission_classes([IsAdmin])
def retreive_number_of_custom_users_view(request):
    custom_users = CustomUser.objects.all()
    total = custom_users.count()
    return response.Response({
        'message': 'Successful',
        'total': total
    }, status=status.HTTP_200_OK)

# function to enable admin view the number of parents
@api_view(['GET'])
@permission_classes([IsParentAdminTeacher])
def retreive_number_of_parents_view(request):
    parents = Parent.objects.all()
    total = parents.count()
    return response.Response({
        'message': 'Successful',
        'Total': total
    })

# function to enable admin retreive number of students
@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def retreive_number_of_students_view(request):
    students = Student.objects.all()
    total = students.count()
    return response.Response({
        'message': 'Successful',
        'Total': total
    })

# Teacher to create an announcement
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_announcement_teacher_view(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return response.Response({'message': 'Successful'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get the student exam marks by an admin or teacher
@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def get_student_exam_marks_admin_teacher_view(request, student):
    student = ExamGrading.objects.get(student=student)
    serializer = ExamGradingSerializer(student)

    return response.Response({
        'message': 'Successful',
        'Results': serializer.data
    })

