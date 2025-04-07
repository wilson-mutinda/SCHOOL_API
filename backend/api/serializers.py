from rest_framework import serializers
import re
from django.core.validators import RegexValidator
from datetime import timedelta, date
from django.utils import timezone

from .models import CustomUser, Role, Parent, Teacher, Student, Subject, Class, Stream, Announcement, Exams, Cat

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
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    cat_code = serializers.CharField(read_only=True)

    class Meta:
        model = Cat
        fields = ['id', 'cat_teacher', 'cat_name', 'class_name', 'stream_name', 'class_name_id', 'stream_name_id', 'content', 'start_time', 'end_time', 'cat_code']

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
