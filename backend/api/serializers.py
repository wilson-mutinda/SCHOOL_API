from rest_framework import serializers
import re
from django.core.validators import RegexValidator
from datetime import timedelta, date, datetime
from django.utils import timezone

from .models import (
    CustomUser, Role, Parent, Teacher, 
    Student, Subject, Class, Stream, 
    Announcement, CatGrading, Cats
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

# Cat Serializer
class CatSerializer(serializers.ModelSerializer):

    cat_name = serializers.CharField()
    cat_teacher = serializers.CharField(source='cat_teacher.teachers.teacher_code', read_only=True)
    content = serializers.CharField()
    cat_class = ClassSerializer()
    cat_stream = StreamSerializer()
    subject = SubjectSerializer()
    duration = serializers.DurationField(default=timedelta(minutes=40))
    date_done = serializers.DateField(format="%Y:%M:%d")
    start_time = serializers.TimeField(format="%H:%M:%s")
    cat_code = serializers.CharField(read_only=True)
    end_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Cats
        fields = ['id', 'cat_name', 'cat_teacher', 'content', 'cat_class', 'cat_stream', 'subject', 'duration', 'date_done', 'start_time', 'cat_code', 'end_time']

    def validate_duration(self, data):
        if data != timedelta(minutes=40):
            raise serializers.ValidationError('Duration is only 40 minutes!')
        return data
    
    def create(self, validated_data):

        validated_data['cat_teacher'] = self.context['request'].user

        class_info = validated_data.pop('cat_class')
        class_name = class_info.get('name')

        try:
            c_name = Class.objects.get(name=class_name)
        except Class.DoesNotExist:
            raise serializers.ValidationError({'cat_class': 'Class not available'})
        
        validated_data['cat_class'] = c_name
        
        stream_info = validated_data.pop('cat_stream')
        stream_name_raw = stream_info.get('name')

        stream_class_info = stream_info.get('class_name')
        stream_class_name = stream_class_info.get('name')

        composed_stream_name = f'{stream_class_name}{stream_name_raw}'

        try:
            s_name = Stream.objects.get(stream_name__iexact=composed_stream_name)
        except Stream.DoesNotExist:
            raise serializers.ValidationError({'cat_stream': 'Stream not available'})
        
        validated_data['cat_stream'] = s_name

        
        subject_details = validated_data.pop('subject')
        subject_name = subject_details.get('name')

        try:
            sub_name = Subject.objects.get(name=subject_name)
            if sub_name.name.lower() == 'english':
                validated_data['is_english'] = True

            if sub_name.name.lower() == 'kiswahili':
                validated_data['is_kiswahili'] = True

            if sub_name.name.lower() == 'maths':
                validated_data['is_maths'] = True

            if sub_name.name.lower() == 'chemistry':
                validated_data['is_chemistry'] = True

            if sub_name.name.lower() == 'physics':
                validated_data['is_physics'] = True

            if sub_name.name.lower() == 'biology':
                validated_data['is_biology'] = True

            if sub_name.name.lower() == 'history':
                validated_data['is_history'] = True

            if sub_name.name.lower() == 'cre':
                validated_data['is_cre'] = True

            if sub_name.name.lower() == 'geography':
                validated_data['is_geography'] = True

            if sub_name.name.lower() == 'business_studies':
                validated_data['is_business_studies'] = True

            if sub_name.name.lower() == 'computer_studies':
                validated_data['is_computer_studies'] = True

            if sub_name.name.lower() == 'agriculture':
                validated_data['is_agriculture'] = True

        except Subject.DoesNotExist:
            raise serializers.ValidationError({'subject': 'Invalid Subject'})
        
        validated_data['subject'] = sub_name

        return super().create(validated_data)
    
# Cat Grading Serializer
class CatGradingSerializer(serializers.ModelSerializer):

    cat_name = serializers.CharField()
    student = serializers.CharField()
    subject = serializers.CharField()

    supervisor = serializers.CharField(source='supervisor.teachers.teacher_code', read_only=True)
    marks = serializers.IntegerField()
    date_graded = serializers.DateTimeField(read_only=True)
    grade = serializers.CharField(read_only=True)

    class Meta:
        model = CatGrading
        fields = ['id', 'cat_name', 'supervisor', 'student', 'marks', 'subject', 'grade', 'date_graded']

    # validate marks
    def validate_marks(self, marks):
        if marks <= 0 :
            raise serializers.ValidationError({'marks': 'Cat Cannot be a zero! Put a 1 instead!'})
        
        if marks > 40:
            raise serializers.ValidationError({'marks': 'Cat cannot be more than 40 marks'})

    def create(self, validated_data):

        # assign supervisor automatically
        validated_data['supervisor'] = self.context['request'].user

        # STUDENT CODE
        student_code = validated_data.pop('student')
        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'student': 'Student Code does not exist!'})
        validated_data['student'] = student

        # CAT
        cat_name = validated_data.pop('cat_name')
        try:
            cat = Cats.objects.get(cat_name=cat_name)
        except Cats.DoesNotExist:
            raise serializers.ValidationError({'cat_name': 'CAT Not Found!'})
        validated_data['cat_name'] = cat

        # Subject
        subject_name = validated_data.pop('subject')
        try:
            subject = Subject.objects.get(name=subject_name)

            if subject.name.lower() == 'english':
                validated_data['is_english'] = True
            
            if subject.name.lower() == 'maths':
                validated_data['is_maths'] = True

            if subject.name.lower() == 'kiswahili':
                validated_data['is_kiswahili'] = True

            if subject.name.lower() == 'chemistry':
                validated_data['is_chemistry'] = True

            if subject.name.lower() == 'physics':
                validated_data['is_physics'] = True

            if subject.name.lower() == 'biology':
                validated_data['is_biology'] = True

            if subject.name.lower() == 'geography':
                validated_data['is_geography'] = True

            if subject.name.lower() == 'history':
                validated_data['is_history'] = True

            if subject.name.lower() == 'cre':
                validated_data['is_cre'] = True

            if subject.name.lower() == 'computer_studies':
                validated_data['is_computer_studies'] = True

            if subject.name.lower() == 'business_studies':
                validated_data['is_business_studies'] = True

            if subject.name.lower() == 'agriculture':
                validated_data['is_agriculture'] = True

        except Subject.DoesNotExist:
            raise serializers.ValidationError({'subject': 'Subject does not exist!'})
        
        validated_data['subject'] = subject

        return super().create(validated_data)

