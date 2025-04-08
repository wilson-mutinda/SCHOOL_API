from rest_framework import serializers
import re
from django.core.validators import RegexValidator
from datetime import timedelta, date, datetime
from django.utils import timezone

from .models import (
    CustomUser, Role, Parent, Teacher, 
    Student, Subject, Class, Stream, 
    Announcement, Exams, Cat, Examination, 
    CatResults, CatGrading, ExamGrading
)

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

    def validate_name(self, name):
        expected_roles = ['admin', 'teacher', 'parent', 'student']
        if name not in expected_roles:
            raise serializers.ValidationError(f'Unexpected Role. Please use either of {', '.join(expected_roles)}')
        
        # existing_role = Role.objects.filter(name=name).exists()
        # if existing_role:
        #     raise serializers.ValidationError({'name': 'Role already exists!'})
        return name
    
# Custom User serializer
class CustomUserSerializer(serializers.ModelSerializer):

    role = RoleSerializer(required = False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'role']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password Mismatch!'})
        
        if len(password) < 8:
            raise serializers.ValidationError({'password': 'Password must have at least 8 characters!'})
        
        if not re.search(r'\d', password):
            raise serializers.ValidationError({'password': 'Password should hav both characters and digits!'})
        
        return data
    
    # Capitalize first name
    def capitalize_first_name(self, first_name):
        return first_name.capitalize()
    
    # capitalize lastname
    def capitalize_last_name(self, last_name):
        return last_name.capitalize()
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # pop role and save it to Role
        role_data = validated_data.pop('role')
        role_name = role_data.get('name')

        if role_name == 'admin':
            validated_data['is_admin'] = True
            validated_data['is_staff'] = True
        elif role_name == 'teacher':
            validated_data['is_teacher'] = True
        elif role_name == 'parent':
            validated_data['is_parent'] = True
        elif role_name == 'student':
            validated_data['is_student'] = True

        role, _ = Role.objects.get_or_create(name=role_name)

        # create customUSer
        user = CustomUser.objects.create_user(role=role, **validated_data)
        return user
    
# Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    phone = serializers.CharField(validators = [
        RegexValidator(regex=r'(01|07)\d{8}', message='Invalid Phone Number!')
    ])
    profile_picture = serializers.ImageField()
    address = serializers.CharField()
    teacher_code = serializers.CharField(read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'phone', 'profile_picture', 'address', 'teacher_code']

    def validate_phone(self, phone):
        if len(phone) != 10:
            raise serializers.ValidationError({'phone': 'Invalid Phone Number!'})
        
        return phone
    
    # Capitalize the first character
    def validate_address(self, address):
        return address.capitalize()
    
    def create(self, validated_data):
        print("Validated Data:", validated_data)

        # filter the user data from the validated data
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')

        user_role = user_data.pop('role', None)
        # if not user_role or not user_role.get('name'):
        #     raise serializers.ValidationError({'role': 'Role name is required'})
        role_name = user_role.get('name')

        # Role name should be teacher only
        if role_name != 'teacher':
            raise serializers.ValidationError({'name': 'Invalid Role! Use "teacher" instead'})
        
        role, _ = Role.objects.get_or_create(name = role_name)

        # set is_teacher_true before creating user
        user_data['is_teacher'] = True


        # create customuser
        user = CustomUser.objects.create_user(role = role, **user_data)

        # create_teacher
        teacher = Teacher.objects.create(user=user, **validated_data)
        print("Teacher Created:", teacher)
        return teacher
    
# Parent Serializer
class ParentSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    phone = serializers.CharField(validators = [
        RegexValidator(regex=r'(01|07)\d{8}', message="Invali Phone Number!")
    ])
    profile_picture = serializers.ImageField()
    address = serializers.CharField()
    parent_code = serializers.CharField(read_only = True)
    class Meta:
        model = Parent
        fields = ['id', 'user', 'phone', 'profile_picture', 'address', 'parent_code']

    def validate_phone(self, phone):
        if len(phone) != 10:
            raise serializers.ValidationError({'phone': 'Invalid Phone Number!'})
        return phone
    
    def validate_address(self, address):
        return address.capitalize()
    
    def create(self, validated_data):
        print("Validated Data:", validated_data)
        # get a user data from the validated data
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')

        user_role = user_data.pop('role', None)
        role_name = user_role.get('name')

        # ensure user role is parent
        if role_name != 'parent':
            raise serializers.ValidationError({'name': "Invalid Role. Role should be 'parent'"})
        
        role, _ = Role.objects.get_or_create(name = role_name)

        # set is_parent true before creating a custom user
        user_data['is_parent'] = True

        # create custom user
        user = CustomUser.objects.create_user(role=role, **user_data)

        # create parent
        parent = Parent.objects.create(user=user, **validated_data)
        return parent
    
# Student serializer
class StudentSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    parent_code = serializers.CharField()
    parent_email = serializers.EmailField()
    student_code = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'parent_code', 'parent_email', 'student_code']

    # lfunction to check parent code and parent_email exist
    def validate(self, data):
        parent_email = data.get('parent_email')
        parent_code = data.get('parent_code')

        # check if a parent exists with both the matchiong code and email via related customuser
        if not Parent.objects.filter(user__email=parent_email, parent_code=parent_code).exists():
            raise serializers.ValidationError('Parent code and Email do not match or do not exist!')
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password', None)

        user_role = user_data.pop('role', None)
        role_name = user_role.get('name')

        # role name should be student only
        if role_name != 'student':
            raise serializers.ValidationError({'name': "Role should be a student"})
        user_data['is_student'] = True
        role, _ = Role.objects.get_or_create(name=role_name)

        user_data['email'] = Student.generate_student_email(user_data['first_name'], user_data['last_name'])

        user = CustomUser.objects.create_user(role=role, **user_data)

        student = Student.objects.create(user=user, **validated_data)
        return student
    
# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    class Meta:
        model = Subject
        fields = ['id', 'name']

    # Ensure only valid subject names are saved
    def validate_name(self, name):
        expected_names = ['maths', 'kiswahili', 'english', 'chemistry', 'physics', 'biology', 'history', 'geography', 'CRE', 'business studies', 'agriculture', 'computer studies']
        if name.lower() not in expected_names:
            raise serializers.ValidationError({'name': f'Invalid Subject Name, Instead use {', '.join(expected_names)}'})
        return name.capitalize()
    
    # create a subject and save in  the dbase
    def create(self, validated_data):
        return super().create(validated_data)
    
# class serializer
class ClassSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    class Meta:
        model = Class
        fields = ['id', 'name']

    # validate class names
    def validate_name(self, name):
        expected_class_names = ['f1', 'f2', 'f3', 'f4']
        if name.lower() not in expected_class_names:
            raise serializers.ValidationError({'name': f'Invalid class names! Instead use {', '.join(expected_class_names)}'})
        return name.capitalize()
    
# stream serializer
class StreamSerializer(serializers.ModelSerializer):

    class_name = ClassSerializer()
    stream_name = serializers.CharField(read_only=True)
    class Meta:
        model = Stream
        fields = ['id', 'class_name', 'name', 'stream_name']

    # vlaidate the stream names
    def validate_name(self, name):
        expected_stream_name = ['e', 'w']
        if name.lower() not in expected_stream_name:
            raise serializers.ValidationError({'name': f'Invalid stream name!Instead use {', '.join(expected_stream_name)}'})
        return name.capitalize()
    
    # create a stream with its class name
    def create(self, validated_data):
        class_data = validated_data.pop('class_name')
        class_name_value = class_data.get('name')

        try:
            class_instance = Class.objects.get(name__iexact=class_name_value)
        except Class.DoesNotExist:
            raise serializers.ValidationError({'class_name': f'Class "{class_name_value}" does not exist.'})
        
        # capitalize and validate the strem name
        stream_name = validated_data.get('name').capitalize()

        # create a stream
        stream = Stream.objects.create(class_name=class_instance, name=stream_name)
        return stream
    
# Announcement Serializer
class AnnouncementSerializer(serializers.ModelSerializer):

    title = serializers.CharField()
    description = serializers.CharField()
    date_created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    created_by = serializers.CharField(source = 'created_by.username', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'description', 'date_created', 'created_by', 'target_teachers', 'target_students','target_admins', 'target_parents']

    def create(self, validated_data):
        # default to false if not provided
        validated_data['target_parents'] = validated_data.get('target_parents', False)
        validated_data['target_students'] = validated_data.get('target_students', False)
        validated_data['target_admins'] = validated_data.get('target_admins', False)
        validated_data['target_teachers'] = validated_data.get('target_teachers', False)

        return super().create(validated_data)

# exam serializer  
class ExamSerializer(serializers.ModelSerializer):
    # Display only
    exam_teacher_display = serializers.CharField(source='exam_teacher.teachers.teacher_code', read_only=True)

    class_name = ClassSerializer(read_only=True)
    stream_name = StreamSerializer(read_only=True)
    class_name_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True, source='class_name')
    stream_name_id = serializers.PrimaryKeyRelatedField(queryset=Stream.objects.all(), write_only=True, source='stream_name')

    # Writable teacher field
    exam_teacher = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    duration = serializers.DurationField(default=timedelta(hours=2))
    time_taken = serializers.DurationField(read_only=True)
    time_remaining = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    teacher_code = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    exam_code = serializers.CharField(read_only=True)

    class Meta:
        model = Exams
        fields = [
            'id', 'exam_teacher', 'exam_teacher_display', 'teacher_code', 'exam_name',
            'class_name', 'stream_name', 'class_name_id', 'stream_name_id',
            'content', 'exam_date', 'duration', 'time_taken', 'time_remaining',
            'is_active', 'start_time', 'end_time', 'date_created', 'exam_code'
        ]

    def get_teacher_code(self, obj):
        if hasattr(obj.exam_teacher, 'teachers'):
            return obj.exam_teacher.teachers.teacher_code
        return None

    def get_time_remaining(self, obj):
        return obj.time_remaining().total_seconds() if obj.time_remaining() else None

    def get_is_active(self, obj):
        return obj.is_active()

# Cat Serializer
class CatSerializer(serializers.ModelSerializer):

    cat_teacher = serializers.CharField(source='cat_teacher.teachers.teacher_code', read_only=True)
    cat_name = serializers.CharField()

    class_name = ClassSerializer(read_only=True)
    stream_name = StreamSerializer(read_only=True)

    class_name_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True, source='class_name')
    stream_name_id = serializers.PrimaryKeyRelatedField(queryset=Stream.objects.all(), write_only=True, source='stream_name')

    content = serializers.CharField()
    cat_date = serializers.DateField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    cat_code = serializers.CharField(read_only=True)

    class Meta:
        model = Cat
        fields = ['id', 'cat_teacher', 'cat_name', 'class_name', 'stream_name', 'class_name_id', 'stream_name_id', 'content', 'cat_date', 'start_time', 'end_time', 'cat_code']

    # validate start time
    def validate_start_time(self, start_time):
        now = timezone.now()
        if start_time < now:
            raise serializers.ValidationError('Start time should be in future!')
        return start_time

    # validate end time
    def validate_end_time(self, end_time):
        now = timezone.now()
        if end_time < now:
            raise serializers.ValidationError('End time should be in future!')
        return end_time
    
    # validate cat dates
    def validate_cat_date(self, cat_date):
        today = date.today()
        if cat_date < today:
            raise serializers.ValidationError({'cat_date': 'Cat cannot be in past!'})

    # validate start time and end time
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({'start_time': 'Invalid Time Configuration!'})
        return data
    
    def create(self, validated_data):
        validated_data['cat_teacher'] = self.context['request'].user
        return super().create(validated_data)
    
# Examination serializer
class ExaminationSerializer(serializers.ModelSerializer):

    exam_name = serializers.CharField()
    exam_teacher = serializers.CharField(source='exam_teacher.teachers.teacher_code', read_only=True)

    class_name = ClassSerializer(read_only=True)
    stream_name = StreamSerializer(read_only=True)
    
    class_name_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True, source='class_name')
    stream_name_id = serializers.PrimaryKeyRelatedField(queryset=Stream.objects.all(), write_only=True, source='stream_name')

    exam_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    content = serializers.CharField()
    exam_code = serializers.CharField(read_only=True)

    class Meta:
        model = Examination
        fields = ['id', 'exam_name', 'exam_teacher', 'class_name', 'stream_name', 'class_name_id', 'stream_name_id', 'exam_date', 'start_time', 'end_time', 'content', 'exam_code']

    # validate start time
    def validate_start_time(self, start_time):
        return start_time
    
    # validate end time
    def validate_end_time(self, end_time):
        return end_time
        
    def validate(self, data):
        exam_date = data['exam_date']
        start_time = data['start_time']
        end_time = data['end_time']

        start = datetime.combine(exam_date, start_time)
        end = datetime.combine(exam_date, end_time)

        # Make start and end timezone-aware
        if timezone.is_naive(start):
            start = timezone.make_aware(start)
        if timezone.is_naive(end):
            end = timezone.make_aware(end)

        now = timezone.now()

        if start < now:
            raise serializers.ValidationError({'start_time': 'Invalid Date Configuration. Please retry!'})

        if end < now:
            raise serializers.ValidationError({'end_time': 'Invalid Date Configuration!'})

        if start >= end:
            raise serializers.ValidationError({'start_time': 'Start time must be before the end time!'})

        if (end - start) > timedelta(hours=2):
            raise serializers.ValidationError('Exam can only last a maximum of 2 hours!')

        return data
    
    def create(self, validated_data):
        validated_data['exam_teacher'] = self.context['request'].user
        return super().create(validated_data)
    

# Cat Result serializer
class CatResultSerializer(serializers.ModelSerializer):

    marks = serializers.IntegerField()
    grade = serializers.CharField(read_only=True)

    cat_name = CatSerializer(read_only=True)
    cat_name_id = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all(), write_only=True, source='cat_name')

    cat_teacher = serializers.CharField(source='cat_teacher.teachers.teacher_code', read_only=True)

    cat_student = serializers.CharField(source='cat_student.students.student_code', read_only=True)
    cat_student_code = serializers.CharField(write_only=True)

    cat_subject = SubjectSerializer(read_only=True)
    cat_subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='cat_subject', write_only=True)

    class Meta:
        model = CatResults
        fields = ['id', 'marks', 'grade', 'cat_name', 'cat_name_id', 'cat_teacher', 'cat_student', 'cat_student_code', 'cat_subject', 'cat_subject_id']

    # validate marks to below at most 30
    def validate_marks(self, marks):
        if marks <= 0 or marks >30:
            raise serializers.ValidationError({'marks': 'Invalid Marks!'})
        return marks
    
    def create(self, validated_data):
        # extract and remove student_code from validated_data
        student_code = validated_data.pop('cat_student_code')

        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'cat_student_code': 'Student with this code does not exist!'})
        
        # assign actual objects to required fields
        validated_data['cat_student'] = student
        validated_data['cat_teacher'] = self.context['request'].user
        return super().create(validated_data)

# Cat Grading Serailizer
class CatGradingSerializer(serializers.Serializer):

    cat_name_id = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all())
    cat_student_code = serializers.CharField()
    subjects = serializers.ListField(
        child = serializers.DictField(
            child=serializers.IntegerField(),
        ),
        help_text = 'List of subjects with subject_id and cat_marks'
    )

    def validate(self, data):
        if not data.get('subjects'):
            raise serializers.ValidationError('At least one subject is required!')
        return data
    
    def create(self, validated_data):
        cat_name = validated_data['cat_name_id']
        student_code = validated_data['cat_student_code']
        subject_data_list = validated_data['subjects']
        teacher = self.context['request'].user

        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'cat_student_code': 'Invalid Student Code'})
        
        graded_subjects = []

        for entry in subject_data_list:
            subject_id = entry.get('subject_id')
            marks = entry.get('cat_marks')

            try:
                subject = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                raise serializers.ValidationError({'subject_id': f'Subject ID {subject_id} not found'})
            
            grading = CatGrading.objects.create(
                cat_name=cat_name,
                cat_teacher = teacher,
                cat_student = student,
                cat_subject = subject,
                cat_marks = marks
            )
            graded_subjects.append(grading)
        return graded_subjects
    
# serializer to handle examGrading
class ExamGradingSerializer(serializers.ModelSerializer):

    exam_name = ExamSerializer(read_only=True)
    exam_name_id = serializers.PrimaryKeyRelatedField(queryset=Exams.objects.all(), source='exam_name', write_only=True)

    exam_teacher = serializers.CharField(source='exam_teacher.teachers.teacher_code', read_only=True)

    exam_student = StudentSerializer(read_only=True)
    exam_student_code = serializers.CharField(write_only=True)

    exam_subject = ExamSerializer(read_only=True)
    exam_subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='exam_subject', write_only=True)

    exam_marks = serializers.IntegerField()
    exam_grade = serializers.CharField(read_only=True)

    class Meta:
        model = ExamGrading
        fields = [
            'id', 'exam_name', 'exam_name_id', 'exam_teacher', 'exam_student', 
            'exam_student_code', 'exam_subject', 'exam_subject_id', 'exam_marks', 'exam_grade', 
            'is_english',
            'is_maths', 'is_kiswahili', 'is_chemistry', 'is_physics',
            'is_biology', 'is_history', 'is_geography', 'is_cre',
            'is_business_studies', 'is_agriculture', 'is_computer_studies'
        ]

    # ensure marks are ented and must be more than 0 and less or equal to 100
    def validate_exam_marks(self, marks):
        if not marks:
            raise serializers.ValidationError({'exam_marks': 'Exam Marks Must be provided!'})
        
        if marks <= 0:
            raise serializers.ValidationError({'exam_marks': 'Exam Marks should be more than 0!'})
        
        if marks > 100:
            raise serializers.ValidationError({'exam_marks': 'Exam Marks cannot be more than 100!'})
        
        return marks
    
    def create(self, validated_data):

        # extract student code and ensure its valid
        student_code = validated_data.pop('exam_student_code')

        try:
            student = Student.objects.get(student_code = student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'cat_student_code': 'Student with the code does not exist!'})
        
        validated_data['exam_student'] = student
        validated_data['exam_teacher'] = self.context['request'].user
        return super().create(validated_data)

