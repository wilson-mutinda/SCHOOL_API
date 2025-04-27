from rest_framework import serializers
import re
from django.core.validators import RegexValidator
from datetime import timedelta, date, datetime
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from .models import (
    CustomUser, Role, Parent, Teacher, 
    Student, Subject, Class, Stream, 
    Announcement, CatGrading, Cats, Exam, 
    ExamGrading, CatAndExam, StreamClassSubjects, CatAndExamGrading, 
    FinalGrade, ReportForm, Term, CustomUserAdmin
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
        extra_kwargs = {
            'username': {'validators': []},  # Disable default unique validator
            'email': {'validators': []}      # Disable default unique validator
        }

    def validate(self, data):
        # Skip password validation if this is an update and password isn't being changed
        if self.instance and not data.get('password'):
            data.pop('password', None)
            data.pop('confirm_password', None)
            return data

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password Mismatch!'})
        
        if password and len(password) < 8:
            raise serializers.ValidationError({'password': 'Password must have at least 8 characters!'})
        
        if password and not re.search(r'\d', password):
            raise serializers.ValidationError({'password': 'Password should have both characters and digits!'})
        
        return data

    def update(self, instance, validated_data):
        # Handle role data if provided
        role_data = validated_data.pop('role', None)
        if role_data:
            role_name = role_data.get('name')
            role, _ = Role.objects.get_or_create(name=role_name)
            instance.role = role

        # Update password if provided
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
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
    
# Class CustomuserAdmin serializer
class CustomUserAdminSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='admin', read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserAdmin
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'role']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password Mismatch!'})
        
        if password and len(password) < 8:
            raise serializers.ValidationError({'password': 'Passwword should have at least 8  characters'})
        
        if password and not re.search(r'\d', password):
            raise serializers.ValidationError({'password': 'Password should have both characters and digits!'})
        
        return data
    
    def create(self, validated_data):

        validated_data.pop('confirm_password', None)
        # create_role
        role, _ = Role.objects.get_or_create(name='admin')
        validated_data['first_name'] = validated_data['first_name'].title()
        validated_data['last_name'] = validated_data['last_name'].title()
        validated_data['password'] = make_password(validated_data['password'])

        # Ensure flags
        validated_data['is_admin'] = True
        validated_data['is_staff'] = True
        validated_data['is_superuser'] = True

        # create user
        user = CustomUser.objects.create_user(role=role, **validated_data)

        # save customuseradmin separately
        CustomUserAdmin.objects.create(
            role='admin',
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            is_teacher=False,
            is_student=False,
            is_parent=False,
            password=user.password
        )
        return user
    
# Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    phone = serializers.CharField(validators = [
        RegexValidator(regex=r'(01|07)\d{8}', message='Invalid Phone Number!')
    ])
    profile_picture = serializers.ImageField(required=False)
    address = serializers.CharField()
    teacher_code = serializers.CharField(read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'phone', 'profile_picture', 'address', 'teacher_code']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

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
    
    # def update(self, instance, validated_data):
    # # Handle user data
    #     user_data = validated_data.pop('user', {})
    #     user = instance.user
        
    #     # Update user fields
    #     for attr, value in user_data.items():
    #         if attr == 'password':
    #             user.set_password(value)
    #         else:
    #             setattr(user, attr, value)
    #     user.save()
        
    #     # Update teacher fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
        
    #     return instance
    
# Parent Serializer
class ParentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    phone = serializers.CharField(validators=[
        RegexValidator(regex=r'(01|07)\d{8}', message="Invalid Phone Number!")
    ])
    profile_picture = serializers.ImageField()
    address = serializers.CharField()
    parent_code = serializers.CharField(read_only=True)

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
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')
        user_role = user_data.pop('role', None)
        role_name = user_role.get('name')

        if role_name != 'parent':
            raise serializers.ValidationError({'name': "Invalid Role. Role should be 'parent'"})

        role, _ = Role.objects.get_or_create(name=role_name)
        user_data['is_parent'] = True
        user = CustomUser.objects.create_user(role=role, **user_data)
        parent = Parent.objects.create(user=user, **validated_data)
        return parent

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', {})
        user_instance = instance.user

        # Handle fields inside user
        for attr, value in user_data.items():
            if attr in ['confirm_password', 'role']:  # ignore these on update
                continue
            setattr(user_instance, attr, value)

        user_instance.save()

        # Update parent instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    
# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    parent_code = serializers.CharField()
    parent_email = serializers.EmailField()
    student_code = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'parent_code', 'parent_email', 'student_code']

    def validate(self, data):
        parent_email = data.get('parent_email')
        parent_code = data.get('parent_code')

        if not Parent.objects.filter(user__email=parent_email, parent_code=parent_code).exists():
            raise serializers.ValidationError('Parent code and Email do not match or do not exist!')

        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user_serializer = CustomUserSerializer(
                instance.user, 
                data=user_data, 
                partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError({'user': user_serializer.errors})

        # Update student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password', None)

        user_role = user_data.pop('role', {'name': 'student'})
        role_name = user_role.get('name')

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
    
# stream_classtudent code serializer
class StreamClassSubjectSerializer(serializers.ModelSerializer):

    student_code = serializers.CharField()
    student_teacher = serializers.CharField(source='student_teacher.teachers.teacher_code', read_only=True)
    student_class = serializers.CharField(read_only=True)
    student_stream = serializers.CharField(read_only=True)
    subject_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = StreamClassSubjects
        fields = ['id', 'student_code', 'student_teacher', 'student_class', 'student_stream', 'subject_count']

    # function to validate the student code
    def validate_student_code(self, code):

        if not code.startswith('S-') or not code[2:].isdigit():
            raise serializers.ValidationError({'student_code': 'Student Code should start with "S-" followed by numbers. Eg. S-001'})
        return code
    
    def create(self, validated_data):
        student_code = validated_data.get('student_code')

        # get the logged in teacher dynamically
        validated_data['student_teacher'] = self.context['request'].user

        # Check if the student exists in Student table
        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'student_code': 'Student does not exist in records!'})
        
        student_class_name = self.context.get('student_class')
        if not student_class_name:
            raise serializers.ValidationError({'student_class': 'Student class is not specified in context!'})
        

        try:
            student_class = Class.objects.get(name__iexact=student_class_name)
        except Class.DoesNotExist:
            raise serializers.ValidationError({'student_class': 'Class Does  Not Exist!'})
        
        # Count how many students already assigned to this class
        class_students = StreamClassSubjects.objects.filter(student_class=student_class.name)

        if class_students.count() >= 40:
            raise serializers.ValidationError({'student_class': 'Maximum number of students (40) reached for this class.'})
        
        # Assign stream based on existing student count
        stream_name = 'E' if class_students.count() < 20 else 'W'

        validated_data['student_class'] = student_class.name
        validated_data['student_stream'] = stream_name

        return super().create(validated_data)
    
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
    
# Term Serializer
class TermSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    class Meta:
        model = Term
        fields = ['id', 'name']

    # validate term name
    def validate_name(self, term):
        expected_names = ['term1', 'term1', 'term3']
        normalized_names = term.lower()

        if normalized_names not in expected_names:
            raise serializers.ValidationError({'name': f'Term name not found. Please select from list: {', '.join(expected_names)}'})
        return term
    
    def create(self, validated_data):
        term_name = validated_data['name']
        if Term.objects.filter(name=term_name).exists():
            raise serializers.ValidationError({'name': f'Name ({term_name}) Already exists!'})
        validated_data['name'] = validated_data['name'].title()
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
    cat_term = serializers.CharField()

    class Meta:
        model = Cats
        fields = [
            'id', 'cat_name', 'cat_teacher', 'content', 
            'cat_class', 'cat_stream', 'subject', 'duration', 
            'date_done', 'start_time', 'cat_code', 'end_time', 
            'cat_term'
        ]

    # validate duration
    def validate_duration(self, data):
        if data != timedelta(minutes=40):
            raise serializers.ValidationError('Duration is only 40 minutes!')
        return data
    
    # validate term
    def validate_cat_term(self, term):
        normalized_name = term.lower()
        expected_terms = ['term1', 'term2', 'term3']

        if normalized_name not in expected_terms:
            raise serializers.ValidationError({'cat_term': f'Term Not Allowed. Please use rither of: {', '.join(expected_terms)}'})
        return term
    
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

# exam serializer
class ExamSerializer(serializers.ModelSerializer):

    exam_name = serializers.CharField()
    exam_teacher = serializers.CharField(source='exam_teacher.teachers.teacher_code', read_only=True)
    content = serializers.CharField()

    exam_class = serializers.CharField()
    exam_stream = serializers.CharField()

    subject = serializers.CharField()
    duration = serializers.DurationField()

    date_done = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField(read_only=True)

    exam_code = serializers.CharField(read_only=True)
    exam_term = serializers.CharField()
    class Meta:
        model = Exam
        fields = [
            'id', 'exam_name', 'exam_teacher', 'content', 
            'exam_class', 'exam_stream', 'subject', 'duration', 
            'date_done', 'start_time', 'end_time', 'exam_code', 'exam_term'
        ]

    # validate exam term
    def validate_exam_term(self, term):
        normalized_name = term.lower()
        expected_names = ['term1', 'term2', 'term3']

        if normalized_name not in expected_names:
            raise serializers.ValidationError({'term_name': f'Invalid Term. Please use one of: {', '.join(expected_names)}'})
        return term

    # validate the duration
    def validate_duration(self, data):
        if data < timedelta(hours=2):
            raise serializers.ValidationError('Duration should not be less than 2 hours!')
        return data
    
    # function to validate the subject
    def validate_subject(self, subject):
        expected_studies = [
            'english', 'maths', 'kiswahili',
            'chemistry', 'physics', 'biology',
            'history', 'geography', 'cre',
            'business_studies', 'computer_studies', 'agriculture'
        ]

        # Normalize to lower case
        subject_normalized = subject.lower().replace(" ", "_")
        if not subject_normalized in expected_studies:
            readable_subjects = [s.replace(" ", "_").title() for s in expected_studies]
            raise serializers.ValidationError({'subject': f'Unexpected subject name. Please use one of {', '.join(readable_subjects)}'})
        return subject
    
    # validate the exam class
    def validate_exam_class(self, exam_class):
        expected_classes = ['F1', 'F2', 'F3', 'F4']

        if not exam_class in expected_classes:
            raise serializers.ValidationError({'exam_class': f'Unexpected Class Name. Please use {', '.join(expected_classes).capitalize()}'})
        return exam_class
    
    # validate the stream class
    def validate_exam_stream(self, exam_stream):
        expected_streams = ['W', 'E']
        if exam_stream.upper() not in expected_streams:
            raise serializers.ValidationError({'exam_stream': f'Invalid Exam Stream. Please use {', '.join(expected_streams)}'})
        return exam_stream
    
    # validate the date done
    def validate_date_done(self, date_done):
        if date_done < date.today():
            raise serializers.ValidationError('Invalid Date Entered!')
        return date_done
    
    def create(self, validated_data):
        # get the teacher dynamically from the logged in user
        validated_data['exam_teacher'] = self.context['request'].user

        # save the term name in title form
        validated_data['exam_term'] = validated_data['exam_term'].title()

        # Class
        exam_class = validated_data.pop('exam_class')
        try:
            class_name = Class.objects.get(name=exam_class)
        except Class.DoesNotExist:
            raise serializers.ValidationError({'exam_class': 'Class Does Not Exist!'})
        
        validated_data['exam_class'] = class_name

        # Stream
        exam_stream = validated_data.pop('exam_stream')
        try:
            stream_name = Stream.objects.get(name__iexact=exam_stream)
        except Stream.DoesNotExist:
            raise serializers.ValidationError({'exam_stream': 'Stream Not Valid'})
        
        validated_data['exam_stream'] = stream_name

        # Subject
        subject_name = validated_data.pop('subject')
        try:
            subject = Subject.objects.get(name =subject_name)

            if subject.name.lower() == 'english':
                validated_data['is_english'] = True

            if subject.name.lower() == 'kiswahili':
                validated_data['is_kiswahili'] = True

            if subject.name.lower() == 'maths':
                validated_data['is_maths'] = True

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

            if subject.name.lower() == 'business_studies':
                validated_data['is_business_studies'] = True

            if subject.name.lower() == 'computer_studiess':
                validated_data['is_computer_studies'] = True

            if subject.name.lower() == 'agriculture':
                validated_data['is_agriculture'] = True

        except Subject.DoesNotExist:
            raise serializers.ValidationError({'subject': 'Subject Does Not Exist!'})
        
        validated_data['subject'] = subject

        return super().create(validated_data)
    
# Exam Grading Serializer
class ExamGradingSerializer(serializers.ModelSerializer):

    exam_name = serializers.CharField()
    student = serializers.CharField()
    subject = serializers.CharField()

    supervisor = serializers.CharField(source='supervisor.teachers.teacher_code', read_only=True)
    marks = serializers.IntegerField()
    grade = serializers.CharField(read_only=True)
    date_graded = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ExamGrading
        fields = ['id', 'exam_name', 'supervisor', 'student', 'marks', 'subject', 'grade', 'date_graded']

    # validate the subject name
    def validate_subject_name(self, name):
        expected_subject_name = [
            'english', 'maths', 'kiswahili', 'physics',
            'chemistry', 'biology', 'history', 'cre',
            'geography', 'business_studies', 'computer_studies', 'agriculture'
        ]
        if name not in expected_subject_name:
            raise serializers.ValidationError({'subject': f'Subject Does Not Exist. Please select from {', '.join(expected_subject_name).capitalize()}'})
        return name
    
    # validate the student code
    def validate_student(self, code):
        if not code.lower().startswith('s'):
            raise serializers.ValidationError({'student': f'Student Code Should start with {'S'}'})
        return code
    
    # validate the marks
    def validate_marks(self, marks):
        if marks > 60:
            raise serializers.ValidationError({'marks': 'Exam marks should not exceed 100'})
        
        if marks <= 0:
            raise serializers.ValidationError({'marks': 'Exam marks cannot be or less than 0'})
        return marks
    
    def create(self, validated_data):

        # get the supervisor dynamically from the logged in user
        validated_data['supervisor'] = self.context['request'].user

        # Exam
        exam = validated_data.pop('exam_name')
        try:
            exam_name = Exam.objects.get(exam_name = exam)
        except Exam.DoesNotExist:
            raise serializers.ValidationError({'exam_name': 'Exam Does Not Exist!'})
        validated_data['exam_name'] = exam_name

        # Student
        student_info = validated_data.pop('student')
        try:
            student_code = Student.objects.get(student_code=student_info)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'student': 'Student wtih this code does not exist!'})
        validated_data['student'] = student_code

        # Subject
        subject_name = validated_data.pop('subject')
        try:
            subject = Subject.objects.get(name=subject_name)

            if subject.name.lower() == 'english':
                validated_data['is_english'] = True

            if subject.name.lower() == 'kiswaahili':
                validated_data['is_kiswahili'] = True

            if subject.name.lower() == 'maths':
                validated_data['is_maths'] = True

            if subject.name.lower() == 'physics':
                validated_data['is_physics'] = True

            if subject.name.lower() == 'chemistry':
                validated_data['is_chemistry'] = True

            if subject.name.lower() == 'biology':
                validated_data['is_biology'] = True

            if subject.name.lower() == 'geography':
                validated_data['is_geography'] = True

            if subject.name.lower() == 'history':
                validated_data['is_history'] = True

            if subject.name.lower() == 'cre':
                validated_data['is_cre'] = True

            if subject.name.lower() == 'agriculture':
                validated_data['is_agriculture'] = True

            if subject.name.lower() == 'computer_studies':
                validated_data['is_computer_studies'] = True

            if subject.name.lower() == 'business_studies':
                validated_data['is_business_studies'] = True

        except Subject.DoesNotExist:
            raise serializers.ValidationError({'subject': 'Subject Does Not Exist!'})
        validated_data['subject'] = subject
        return super().create(validated_data)
    
# cat and exam serializer
class CatAndExamSerailizer(serializers.ModelSerializer):

    class_name = serializers.CharField()
    stream_name = serializers.CharField()
    class_teacher = serializers.CharField(source='class_teacher.teachers.teacher_code', read_only=True)
    class_student = serializers.CharField()
    subject = serializers.CharField()
    student_cat = serializers.IntegerField(read_only=True)
    student_exam = serializers.IntegerField(read_only=True)

    class Meta:
        model = CatAndExam
        fields = ['id', 'class_name', 'stream_name', 'class_teacher', 'class_student', 'subject', 'student_cat', 'student_exam']

    # validate the subjects to be entered
    def validate_subject(self, subject_name):
        expected_subject_names = [
            'english', 'maths', 'kiswahili', 'physics',
            'chemistry', 'biology', 'geography', 'history',
            'cre', 'business_studies', 'computer_studies', 'agriculture'
        ]

        cleaned_subject_name = subject_name.lower().replace(" ", "_")

        if cleaned_subject_name not in expected_subject_names:
            raise serializers.ValidationError({'subject': f'Invalid Subject. Instead use: {', '.join(expected_subject_names)}'})
        return cleaned_subject_name

    # validate the class name
    def validate_class_name(self, class_name):
        expected_class_name = ['F1', 'F2', 'F3' , 'F4']
        cleaned_class_name = class_name.upper().strip()

        if cleaned_class_name not in expected_class_name:
            raise serializers.ValidationError({'class_name': f'Invalid Class Name. Instead use {', '.join(expected_class_name)}'})
        return cleaned_class_name
    
    # validate the stream name
    def validate_stream_name(self, stream_name):
        expected_stream_names = ['E', 'W']
        cleaned_stream_name = stream_name.upper().strip()

        if cleaned_stream_name not in expected_stream_names:
            raise serializers.ValidationError({'stream_name': f"Stream Name not Valid. Please use either of {', '.join(expected_stream_names)}"})
        return cleaned_stream_name

    def create(self, validated_data):
        
        # Assign class_teacher dynamically from the logged in teacher
        validated_data['class_teacher'] = self.context['request'].user

        # Stream
        stream = validated_data.pop('stream_name')
        try:
            stream_name = Stream.objects.get(name=stream)
        except Stream.DoesNotExist:
            raise serializers.ValidationError({'stream_name': 'Stream Not Found!'})
        validated_data['stream_name'] = stream_name

        # Class
        class_name = validated_data.pop('class_name')
        try:
            name = Class.objects.get(name=class_name)
        except Class.DoesNotExist:
            raise serializers.ValidationError({'class_name': 'Class Not Found!'})
        validated_data['class_name'] = name

        # get the student code, then if it exists, get the subject and its associated cat and exam
        student = validated_data.pop('class_student')
        try:
            student_code = Student.objects.get(student_code = student)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'class_student': 'Student with the code does not exist!'})
        validated_data['class_student'] = student_code

        # Subject
        subject_name = validated_data.pop('subject')
        try:
            subject = Subject.objects.get(name__iexact=subject_name.replace("_", " "))
        except Subject.DoesNotExist:
            raise serializers.ValidationError({'subject': 'Subject does not exist!'})
        validated_data['subject'] = subject

        # Exam
        try:
            exam = ExamGrading.objects.get(student = student_code)
            if exam:
                marks = exam.marks
            exam_marks = marks
        except ExamGrading.DoesNotExist:
            raise serializers.ValidationError({'student_exam': 'Exam Not Done!'})
        validated_data['student_exam'] = exam_marks

        # CAT
        try:
            cat = CatGrading.objects.get(student=student_code)
            if cat:
                marks = cat.marks
            cat_marks = marks
        except CatGrading.DoesNotExist:
            raise serializers.ValidationError({'student_cat': 'Cat Not Done!'})
        validated_data['student_cat'] = cat_marks
        return super().create(validated_data)  

# Cat And Exam Grading
class CatAndExamGradingSerializer(serializers.ModelSerializer):
    student_teacher = serializers.CharField(source='student_teacher.teachers.student_code', read_only=True)
    student_code = serializers.CharField()
    student_subject = serializers.CharField()
    subject_cat_marks = serializers.IntegerField(read_only=True)
    subject_exam_marks = serializers.IntegerField(read_only=True)
    student_class = serializers.CharField(read_only=True)
    student_stream = serializers.CharField(read_only=True)
    subject_total = serializers.IntegerField(read_only=True)
    subject_grade = serializers.CharField(read_only=True)

    class Meta:
        model = CatAndExamGrading
        fields = [
            'id', 'student_teacher', 'student_code', 'student_subject', 
            'subject_cat_marks', 'subject_exam_marks', 'student_class', 'student_stream', 
            'subject_total', 'subject_grade'
        ]

    # validate the student code
    def validate_student_code(self, code):
        if not code.upper().startswith('S-'):
            raise serializers.ValidationError({'student_code': 'Invalid Student Code!'})
        return code
    
    # validate the subject for the student
    def validate_student_subject(self, subject):
        expected_subjects = {
            'english' :'English',
            'kiswahili': 'Kiswahili',
            'maths': 'Maths',
            'chemistry': 'Chemistry',
            'physics': 'Physics',
            'biology': 'Biology',
            'geography': 'Geography',
            'history': 'History',
            'cre': 'Cre',
            'agriculture': 'Agriculture',
            'business_studies': 'Business_Studies',
            'computer_studies': 'Computer_Studies'
        }

        subject_key = subject.lower()
        if subject_key not in expected_subjects:
            allowed_list = ', '.join(expected_subjects.values())
            raise serializers.ValidationError({'student_subject': f'Invalid Subject Name. Indtead, use: {allowed_list}'})
        return expected_subjects[subject_key]

    def create(self, validated_data):
        # Get the teacher automatically
        validated_data['student_teacher'] = self.context['request'].user

        # get the student code
        input_student = validated_data.pop('student_code')
        try:
            Student.objects.get(student_code=input_student)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'student_code': 'Student with the code is not available!'})
        validated_data['student_code'] = input_student

        # Class and stream
        try:
            student = StreamClassSubjects.objects.get(student_code=input_student)
            if student:
                student_class = student.student_class
                student_stream = student.student_stream
            student_class = student_class
            student_stream = student_stream
        except StreamClassSubjects.DoesNotExist:
            raise serializers.ValidationError({'student_class': 'Student not in class'})
        
        validated_data['student_class'] = student_class
        validated_data['student_stream'] = student_stream

        # Subject
        input_subject = validated_data.pop('student_subject')
        try:
            subject = Subject.objects.get(name=input_subject)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({'student_subject'})
        validated_data['student_subject'] = subject

        # get subject cat and exam marks
        try:
            subject_exam_marks = ExamGrading.objects.get(subject=subject)
            exam_marks = subject_exam_marks.marks
        except ExamGrading.DoesNotExist:
            raise serializers.ValidationError({'subject_exam_marks': 'Subject not graded!'})
        validated_data['subject_exam_marks'] = exam_marks

        try:
            subject_cat_marks = CatGrading.objects.get(subject=subject)
            cat_marks = subject_cat_marks.marks
        except CatGrading.DoesNotExist:
            raise serializers.ValidationError({'subject_cat_marks': 'Subject Not Graded!'})
        validated_data['subject_cat_marks'] = cat_marks

        # function to calculate the final grade
        def calculate_grade(total):
            if total >= 70:
                return 'A'
            
            elif total >= 60:
                return 'B'
            
            elif total >= 50:
                return 'C'
            
            elif total >= 40:
                return 'D'
            
            elif total >= 30:
                return 'E'
            
            else:
                return 'FAIL'

        total_marks = exam_marks + cat_marks
        validated_data['subject_total'] = total_marks

        subject_grade = calculate_grade(total_marks)
        validated_data['subject_grade'] = subject_grade

        # assign marks to the specified subject
        if subject.name == 'English':
            validated_data['is_english_cat'] = cat_marks
            validated_data['is_english_exam'] = exam_marks
            validated_data['is_english_total'] = total_marks
            validated_data['is_english_grade'] = subject_grade

        if subject.name == 'Kiswahili':
            validated_data['is_kiswahili_cat'] = cat_marks
            validated_data['is_kiswahili_exam'] = exam_marks
            validated_data['is_kiswahili_total'] = total_marks
            validated_data['is_kiswahili_grade'] = subject_grade

        if subject.name == 'Maths':
            validated_data['is_maths_cat'] = cat_marks
            validated_data['is_maths_exam'] = exam_marks
            validated_data['is_maths_total'] = total_marks
            validated_data['is_maths_grade'] = subject_grade
        
        if subject.name == 'Physics':
            validated_data['is_physics_cat'] = cat_marks
            validated_data['is_physics_exam'] = exam_marks
            validated_data['is_physics_total'] = total_marks
            validated_data['is_physics_grade'] = subject_grade

        if subject.name == 'Chemistry':
            validated_data['is_chemistry_cat'] = cat_marks
            validated_data['is_chemistry_exam'] = exam_marks
            validated_data['is_chemistry_total'] = total_marks
            validated_data['is_chemistry_grade'] = subject_grade

        if subject.name == 'Biology':
            validated_data['is_biology_cat'] = cat_marks
            validated_data['is_biology_exam'] = exam_marks
            validated_data['is_biology_total'] = total_marks
            validated_data['is_biology_grade'] = subject_grade

        if subject.name == 'Geography':
            validated_data['is_geography_cat'] = cat_marks
            validated_data['is_geography_exam'] = exam_marks
            validated_data['is_geography_total'] = total_marks
            validated_data['is_geography_grade'] = subject_grade

        if subject.name == 'Cre':
            validated_data['is_cre_cat'] = cat_marks
            validated_data['is_cre_exam'] = exam_marks
            validated_data['is_cre_total'] = total_marks
            validated_data['is_cre_grade'] = subject_grade

        if subject.name == 'History':
            validated_data['is_history_cat'] = cat_marks
            validated_data['is_history_exam'] = exam_marks
            validated_data['is_history_total'] = total_marks
            validated_data['is_history_grade'] = subject_grade

        if subject.name == 'Business_studies':
            validated_data['is_business_studies_cat'] = cat_marks
            validated_data['is_business_studies_exam'] = exam_marks
            validated_data['is_business_studies_total'] = total_marks
            validated_data['is_business_studies_grade'] = subject_grade

        if subject.name == 'Computer_studies':
            validated_data['is_computer_studies_cat'] = cat_marks
            validated_data['is_computer_studies_exam'] = exam_marks
            validated_data['is_computer_studies_total'] = total_marks
            validated_data['is_computer_studies_grade'] = subject_grade

        if subject.name == 'Agriculture':
            validated_data['is_agriculture_cat'] = cat_marks
            validated_data['is_agriculture_exam'] = exam_marks
            validated_data['is_agriculture_total'] = total_marks
            validated_data['is_agriculture_grade'] = subject_grade

        return super().create(validated_data)

# FinalGrade Serializer
class FinalGradeSerializer(serializers.ModelSerializer):

    student = serializers.CharField()
    teacher = serializers.CharField(source='teacher.teachers.teacher_code', read_only=True)
    total_subjects = serializers.IntegerField(read_only=True)
    total_marks = serializers.IntegerField(read_only=True)
    final_grade = serializers.CharField(read_only=True)

    class Meta:
        model = FinalGrade
        fields = ['id', 'student', 'teacher', 'total_subjects', 'total_marks', 'final_grade']

    # validate the format of the student code
    def validate_student(self, code):
        pattern = r'^S-\d+$'
        if not re.match(pattern, code):
            raise serializers.ValidationError({'student': 'In   valid Student Code. Please use format: S-<number>'})
        return code
    
    def create(self, validated_data):

        # assign teacher dynamically
        validated_data['teacher'] = self.context['request'].user
        student_code = validated_data['student']

        # Student
        try:
            student = CatAndExamGrading.objects.get(student_code = student_code)
            subject_list = []
            subject_marks = []

            if student.is_english_total != 0:
                subject_list.append('English')
                subject_marks.append(student.is_english_total)
            
            if not subject_list:
                raise serializers.ValidationError({'total_subjects': 'No valid subject marks found'})
            
            validated_data['total_subjects'] = len(subject_list)
            validated_data['total_marks'] = sum(subject_marks)

            # function to calcualte the final_grade
            def calculate_final_grade(average):
                if average >= 70:
                    return 'A'
                elif average >= 60:
                    return 'B'
                elif average >= 50:
                    return 'C'
                elif average >= 40:
                    return 'D'
                elif average >= 30:
                    return 'E'
                else:
                    return 'FAIL'
            average = validated_data['total_marks'] / validated_data['total_subjects']
            validated_data['final_grade'] = calculate_final_grade(average)
            validated_data['student'] = student_code
        except CatAndExamGrading.DoesNotExist:
            raise serializers.ValidationError({'student': 'Student Has No Marks!'})
        
        return super().create(validated_data)

# Report form serializer
class ReportFormSerializer(serializers.ModelSerializer):

    class_teacher = serializers.CharField(source='class_teacher.teachers.teacher_code', read_only=True)
    student_code = serializers.CharField()
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    student_class = serializers.CharField(read_only=True)
    student_stream = serializers.CharField(read_only=True)
    student_average_grade = serializers.CharField(read_only=True)
    teacher_remarks = serializers.CharField(read_only=True)
    total_subjects = serializers.IntegerField(read_only=True)
    total_marks = serializers.IntegerField(read_only=True)
    term_name = serializers.CharField(read_only=True)

    class Meta:
        model = ReportForm
        fields = [
            'id', 'class_teacher', 'student_code', 'student_first_name', 
            'student_last_name', 'student_class', 'student_stream', 'student_average_grade', 
            'teacher_remarks', 'total_subjects', 'total_marks', 'term_name'
        ]
    
    # validate the student code
    def validate_student_code(self, code):
        pattern = r'^S-\d+$'
        if not re.match(pattern, code):
            raise serializers.ValidationError({'student_code': 'Invalid Student Code Format,=. Use S-<number> instead!'})
        return code
    
    def create(self, validated_data):

        user = self.context['request'].user
        validated_data['class_teacher'] = user

        student_id = validated_data.get('id')
        

        student_code = validated_data.get('student_code')

        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError({'student_code': "Student Does Not Exist!"})
        
        # assign basic student info
        validated_data['student_first_name'] = student.user.first_name
        validated_data['student_last_name'] = student.user.last_name

        try:
            grading = CatAndExamGrading.objects.filter(student_code=student_code)
        except CatAndExamGrading.DoesNotExist:
            raise serializers.ValidationError({'student_code': 'Grading Records not found!'})
        
        # initialize counters
        total_marks = 0
        total_subjects = 0

        subjects_handled = {
            "English": ("is_english_cat", "is_english_exam", "is_english_total"),
            "Maths": ("is_maths_cat", "is_maths_exam", "is_maths_total"),
            "Kiswahili": ("is_kiswahili_cat", "is_kiswahili_exam", "is_kiswahili_total"),

            "Physics": ("is_physics_cat", "is_physics_exam", "is_physics_total"),
            "Chemistry": ("is_chemistry_cat", "is_chemistry_exam", "is_chemistry_total"),
            "Biology": ("is_biology_cat", "is_biology_exam", "is_biology_total"),

            "Geography": ("is_geography_cat", "is_geography_exam", "is_geography_total"),
            "Cre": ("is_cre_cat", "is_cre_exam", "is_cre_total"),
            "History": ("is_history_cat", "is_history_exam", "is_history_total"),

            "Business_studies": ("is_business_studies_cat", "is_business_studies_exam", "is_business_studies_total"),
            "Computer_studies": ("is_computer_studies_cat", "is_computer_studies_exam", "is_computer_studies_total"),
            "Agriculture": ("is_agriculture_cat", "is_agriculture_exam", "is_agriculture_total"),
        }

        for grade in grading:
            subject = grade.student_subject
            if subject in subjects_handled:
                cat_field, exam_field, total_field = subjects_handled[subject]
                validated_data[cat_field] = getattr(grade, cat_field)
                validated_data[exam_field] = getattr(grade, exam_field)
                validated_data[total_field] = getattr(grade, total_field)

                total_marks += getattr(grade, total_field)
                total_subjects += 1

                validated_data['student_class'] = grade.student_class
                validated_data['student_stream'] = grade.student_stream

        validated_data['total_subjects'] = total_subjects
        validated_data['total_marks'] = total_marks

        # conpute average and remarks
        average = total_marks / total_subjects if total_subjects else 0
        validated_data['student_average_grade'] = f'{average:.2f}'

        if average >= 70:
            validated_data['teacher_remarks'] = 'Excellent'

        elif average >= 50:
            validated_data['teacher_remarks'] = 'Good'

        elif average >= 30:
            validated_data['teacher_remarks'] = 'Fair'

        else:
            validated_data['teacher_remarks'] = 'FAIL'

        # assign term name based on number of existing reports for that student
        existing_terms = ReportForm.objects.filter(student_code=student_code).count()

        if existing_terms == 0:
            validated_data['term_name'] = 'term1'
        elif existing_terms == 1:
            validated_data['term_name'] = 'term2'
        elif existing_terms == 2:
            validated_data['term_name'] = 'term3'
        else:
            raise serializers.ValidationError({'term_name': 'Maximum number of terms (3) already recorded for this student!'})


        return super().create(validated_data)
