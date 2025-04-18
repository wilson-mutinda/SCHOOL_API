from django.shortcuts import render, get_object_or_404

from .models import (
    CustomUser, Role, Parent, Teacher, Student, 
    Subject, Class, Stream, Announcement, CatGrading, 
    Cats, Exam, ExamGrading, CatAndExam, StreamClassSubjects,
    CatAndExamGrading, FinalGrade, ReportForm, Term
)
from .serializers import (
    CustomUserSerializer, RoleSerializer, TeacherSerializer, ParentSerializer, StudentSerializer,
    SubjectSerializer, ClassSerializer, StreamSerializer, AnnouncementSerializer, CatGradingSerializer, 
    CatSerializer, ExamSerializer, ExamGradingSerializer, CatAndExamSerailizer, StreamClassSubjectSerializer,
    CatAndExamGradingSerializer, FinalGradeSerializer, ReportFormSerializer, TermSerializer
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
    
# function class to combine both admin and teacher to have same priviledges
class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_teacher)
    
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
@permission_classes([IsAdminTeacherAnnouncement])
def retreive_teacher_targeted_announcements_view(request):
    announcements = Announcement.objects.filter(target_teachers=True)
    total = announcements.count()
    serailizer = AnnouncementSerializer(announcements, many=True)
    return response.Response({
        'message': 'Successful',
        'Total': total,
        'Announcements': serailizer.data
    }, status=status.HTTP_200_OK)

# retreive the student targeted announcements
@api_view(['GET'])
@permission_classes([IsAdminTeacherAnnouncement])
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
@permission_classes([IsAdminTeacherAnnouncement])
def retreive_parent_targeted_announcements_view(requeest):
    announcements = Announcement.objects.filter(target_parents=True)
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
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_cat_view(request):
    serializer = CatSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Cat Created!'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin to reteive and update a cat
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_cat_admin_view(request, cat_code):
    try:
        cat = Cats.objects.get(cat_code=cat_code)

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
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_cat_grade_view(request):
    serializer = CatGradingSerializer(data=request.data, context = {'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Cat Graded successfully!'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# permit a logged in teacher to create an exam
@api_view(['POST'])
@permission_classes([IsAdminOrTeacher])
def create_exam_view(request):
    serializer = ExamSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Exam Created'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# permit a teacher to grade a student exam
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_exam_grade_view(request):
    serializer = ExamGradingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Exam Graded'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function view to create a cat and exam by an authorized teacher
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_exam_and_cat_view(request):
    serializer = CatAndExamSerailizer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to generate a student with class and stream
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_class_stream_subject_view(request):
    serializer = StreamClassSubjectSerializer(data=request.data, context={'request': request, 'student_class': 'F1'})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function view to calculate the grand total of subject cat and exam
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_overall_subject_grade_view(request):
    serializer = CatAndExamGradingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Successful'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to get the final grade
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_final_grade_view(request):
    serializer = FinalGradeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Grading Successful'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to generate a report form 
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_report_form_view(request):
    serializer = ReportFormSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return response.Response({'message': 'Report Generated!'}, status=status.HTTP_200_OK)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function to calcukate the number of teachers
@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def get_the_number_of_registered_teachers(request):
    teachers = Teacher.objects.all()
    total = teachers.count()

    return response.Response({
        'message': f"Successful",
        'Total': total
    }, status=status.HTTP_200_OK)

# function to ensure admin can view and chane teacher details
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
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
@permission_classes([IsAdminOrTeacher])
def retreive_update_delete_student_info_view(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            student.delete()
            return response.Response({'message': 'Student Deleted'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        return response.Response({'message': 'Student not found!'}, status=status.HTTP_404_NOT_FOUND)

# function to ensure  an admin can view and update parent details
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def retreive_update_delete_parent_info_view(request, parent_code):
    
    try:
        parent = Parent.objects.get(parent_code=parent_code)

        if request.method == 'GET':
            serializer = ParentSerializer(parent)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ParentSerializer(parent, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.errors, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            parent.delete()
            return response.Response({'message': 'Parent Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Parent.DoesNotExist:
        return response.Response({'message': 'Parent Does not Exist!'}, status=status.HTTP_404_NOT_FOUND)
    
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
@permission_classes([IsAdmin])
def retreive_number_of_parents_view(request):
    parents = Parent.objects.all()
    total = parents.count()
    return response.Response({
        'message': 'Successful',
        'Total': total
    })

# function to enable admin retreive number of students
@api_view(['GET'])
@permission_classes([IsAdmin])
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

