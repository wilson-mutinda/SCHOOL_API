from rest_framework import serializers
import re
from django.core.validators import RegexValidator

from .models import CustomUser, Role, Parent, Teacher, Student

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
