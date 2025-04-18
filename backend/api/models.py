from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class for CustomUSer Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is Required!")
        
        if not password:
            raise ValueError("Password is Required!")
        
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
    
# Role model
class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# Custom user class model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)

    # Timestamps
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # status flags
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin  = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'role']

    def __str__(self):
        return f'{self.username} - ({self.role.name})'
    
# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teachers')
    phone = models.CharField(max_length=10, unique=True)
    profile_picture = models.ImageField(upload_to='teacher_profile', blank=True, null=True)
    address = models.TextField()
    teacher_code = models.CharField(max_length=20, unique=True)

    # class method to generate a unique teacher code
    @classmethod
    def generate_teacher_code(cls):
        # filer the last saved teacher instance
        last_teacher = cls.objects.order_by('-id').first()
        if last_teacher and last_teacher.teacher_code:
            try:
                last_code = int(last_teacher.teacher_code.split('-')[1])
                next_code = last_code + 1
            except (IndexError, ValueError):
                next_code = 1
        else:
            next_code = 1
        return f'T-{next_code:03d}'


    def __str__(self):
        return f'{self.user.username} - {self.phone}'
    
    def save(self, *args, **kwargs):
        if not self.teacher_code:
            self.teacher_code = self.generate_teacher_code()
        super().save(*args, **kwargs)
    
    
# parent model
class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=10, unique=True)
    profile_picture = models.ImageField(upload_to='parent_profile', blank=True, null=True)
    address = models.TextField()
    parent_code = models.CharField(max_length=20, unique=True)

    # class method to generate a parent code
    @classmethod
    def generate_parent_code(cls):
        # filter the last saved parent
        last_parent = cls.objects.order_by('-id').first()
        if last_parent and last_parent.parent_code:
            try:
                last_code = int(last_parent.parent_code.split('-')[1])
                next_code = last_code + 1
            except (IndexError, ValueError):
                next_code = 1
        else:
            next_code = 1
        return f'P-{next_code:03d}'

    def __str__(self):
        return f'{self.user.username} - {self.phone}'
    
    def save(self, *args, **kwargs):
        if not self.parent_code:
            self.parent_code = self.generate_parent_code()
        super().save(*args, **kwargs)

# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# student model
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='students')
    parent_code = models.CharField(max_length=100, unique=True)
    parent_email = models.EmailField(unique=True)
    student_code = models.CharField(max_length=100, unique=True)
    subjects = models.ManyToManyField(Subject, related_name='students')

    # class method to calculate student code
    @classmethod
    def generate_student_code(cls):
        # fetch the last student on the dbase
        last_student = cls.objects.order_by('-id').first()
        # if last student is availaleand has code, then get the code itself
        if last_student and last_student.student_code:
            last_code = int(last_student.student_code.split('-')[1])
            next_code = last_code + 1
        else:
            next_code = 1

        return f'S-{next_code:03d}'
    
    # static method to create a student email
    @staticmethod
    def generate_student_email(first_name, last_name):
        # clean names and create base email
        base_email = f'{first_name.strip().lower()}.{last_name.strip().lower()}@bidii.edu'

        # check for uniqueness and append numbers if possible
        counter = 1
        email = base_email
        while CustomUser.objects.filter(email=email).exists():
            email = f'{first_name.strip().lower()}.{last_name.strip().lower()}{counter}@bidii.edu'
            counter += 1
        return email

    def __str__(self):
        return f'{self.user.username} - ({self.parent_code})'
    
    def save(self, *args, **kwargs):
        if not self.student_code:
            self.student_code = self.generate_student_code()

        # generate email if user is being created 
        if not self.user_id:
            self.user.email = self.generate_student_email(self.user.first_name, self.user.last_name)
        super().save(*args, **kwargs)
    
# Class models
class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# Stream models
class Stream(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=100)
    stream_name = models.CharField(max_length=10, unique=True, blank=True)

    # static method/helper to create a stream
    @staticmethod
    def create_stream_name(class_name, name):
        return f'{class_name}{name}'

    def __str__(self):
        return f'{self.class_name.name}{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.stream_name:
            self.stream_name = self.create_stream_name(self.class_name.name, self.name)
        super().save(*args, **kwargs)

# Class Stream model
class StreamClassSubjects(models.Model):
    student_code = models.CharField(max_length=20, unique=True)
    student_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stream_class_subject')
    student_class = models.CharField(max_length=10)
    student_stream = models.CharField(max_length=10)
    subject_count = models.IntegerField()

    is_english = models.BooleanField(default=True)
    is_maths = models.BooleanField(default=True)
    is_kiswahili = models.BooleanField(default=True)

    is_chemistry = models.BooleanField(default=True)
    is_physics = models.BooleanField(default=True)
    is_biology = models.BooleanField(default=True)

    is_geography = models.BooleanField(default=True)
    is_cre = models.BooleanField(default=True)
    is_history = models.BooleanField(default=True)

    is_computer_studies = models.BooleanField(default=True)
    is_business_studies = models.BooleanField(default=True)
    is_agriculture = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.student_code} from {self.student_class}{self.student_stream}'
    
    def save(self, *args, **kwargs):

        subject_fields = [
        'is_maths', 'is_english', 'is_kiswahili', 'is_physics',
        'is_chemistry', 'is_biology', 'is_history', 'is_cre',
        'is_geography', 'is_business_studies', 'is_computer_studies', 'is_agriculture'
    ]
        self.subject_count = sum(1 for field in subject_fields if getattr(self, field, False))
        super().save(*args, **kwargs)
    
# Announcement model
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')

    target_teachers = models.BooleanField(default=False)
    target_admins = models.BooleanField(default=False)
    target_parents = models.BooleanField(default=False)
    target_students = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} created by {self.created_by.username}'
    
# class model to create term
class Term(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# CAT MODEL
class Cats(models.Model):
    cat_name = models.CharField(max_length=200)
    cat_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cats')
    content = models.TextField()
    cat_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='cats')
    cat_stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='cats')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='cats')  
    duration = models.DurationField(default=timedelta(minutes=40))
    date_done = models.DateField()
    start_time = models.TimeField()
    cat_code = models.CharField(max_length=20, unique=True)
    cat_term = models.CharField(max_length=20)
    end_time = models.TimeField()

    is_english = models.BooleanField(default=False)
    is_maths = models.BooleanField(default=False)
    is_kiswahili = models.BooleanField(default=False)

    is_chemistry = models.BooleanField(default=False)
    is_physics = models.BooleanField(default=False)
    is_biology = models.BooleanField(default=False)

    is_geography = models.BooleanField(default=False)
    is_cre = models.BooleanField(default=False)
    is_history = models.BooleanField(default=False)

    is_computer_studies = models.BooleanField(default=False)
    is_business_studies = models.BooleanField(default=False)
    is_agriculture = models.BooleanField(default=False)

    # function to calculate the expected end time
    def calculate_end_time(self):
        full_start = datetime.combine(datetime.today(), self.start_time)
        expected_finish_time = full_start + self.duration
        return expected_finish_time.time()
        

    # class method to create a cat code
    @classmethod
    def generate_cat_code(cls):
        last_cat = cls.objects.order_by('-id').first()

        # if last cat, then get the asssociated code
        if last_cat and last_cat.cat_code:
            last_code = int(last_cat.cat_code.split('-')[1])
            next_code = last_code + 1
        else:
            next_code = 1
        return f'C-{next_code:03d}'

    def __str__(self):
        return f'{self.cat_name} done on {self.date_done} starting at {self.start_time}'
    
    def save(self, *args, **kwargs):
        if not self.cat_code:
            self.cat_code = self.generate_cat_code()

        if not self.end_time:
            self.end_time = self.calculate_end_time()

        super().save(*args, **kwargs)

# CATGRADING MODEL
class CatGrading(models.Model):
    cat_name = models.ForeignKey(Cats, on_delete=models.CASCADE, related_name='cat_grading')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat_grading')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='cat_grading')
    marks = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='cat_grading')
    grade = models.CharField(max_length=10)
    date_graded = models.DateTimeField(auto_now_add=True)

    is_english = models.BooleanField(default=False)
    is_maths = models.BooleanField(default=False)
    is_kiswahili = models.BooleanField(default=False)

    is_chemistry = models.BooleanField(default=False)
    is_physics = models.BooleanField(default=False)
    is_biology = models.BooleanField(default=False)

    is_geography = models.BooleanField(default=False)
    is_cre = models.BooleanField(default=False)
    is_history = models.BooleanField(default=False)

    is_computer_studies = models.BooleanField(default=False)
    is_business_studies = models.BooleanField(default=False)
    is_agriculture = models.BooleanField(default=False)

    # function to calculate the final grade
    def cat_grade(self):
        marks = self.marks
        total_marks = ((marks / 40) * 30)

        if total_marks >= 25:
            return 'A'
        
        elif total_marks >= 20:
            return 'B'
        
        elif total_marks >= 15:
            return 'c'
        
        elif total_marks >= 10:
            return 'D'
        
        elif total_marks >= 5:
            return 'E'
        
        else:
            return 'FAIL'

    def __str__(self):
        return f'{self.cat_name.cat_name} for {self.student.user.username}'
    
    def save(self, *args, **kwargs):
        if not self.grade:
            self.grade = self.cat_grade()
        super().save(*args, **kwargs)

# Exam model
class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    exam_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
    content = models.TextField()
    exam_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    exam_stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    duration = models.DurationField(default=timedelta(hours=2))
    date_done = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    exam_code = models.CharField(max_length=20, unique=True)
    exam_term = models.CharField(max_length=20)

    is_english = models.BooleanField(default=False)
    is_maths = models.BooleanField(default=False)
    is_kiswahili = models.BooleanField(default=False)

    is_chemistry = models.BooleanField(default=False)
    is_physics = models.BooleanField(default=False)
    is_biology = models.BooleanField(default=False)

    is_geography = models.BooleanField(default=False)
    is_cre = models.BooleanField(default=False)
    is_history = models.BooleanField(default=False)

    is_computer_studies = models.BooleanField(default=False)
    is_business_studies = models.BooleanField(default=False)
    is_agriculture = models.BooleanField(default=False)

    # function to calculate the end tome for an exam
    def calculate_end_time(self):
        full_start = datetime.combine(datetime.today(), self.start_time)
        expected_end_time = full_start + self.duration
        return expected_end_time.time()

    # class method to generate the exam code
    @classmethod
    def generate_exam_code(cls):
        last_exam = cls.objects.order_by('-id').first()

        # if last exam, get the exam code
        if last_exam and last_exam.exam_code:
            last_code = int(last_exam.exam_code.split('-')[1])
            next_code = last_code + 1
        else:
            next_code = 1
        return f'E-{next_code:03d}'

    def __str__(self):
        return f'{self.exam_name} - to be done on {self.date_done} at {self.start_time}'
    
    def save(self, *args, **kwargs):
        if not self.exam_code:
            self.exam_code = self.generate_exam_code()

        if not self.end_time:
            self.end_time = self.calculate_end_time()

        super().save(*args, **kwargs)

# Exam Grading model
class ExamGrading(models.Model):
    exam_name = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_grading')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_grading')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_grading')
    marks = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_grading')
    grade = models.CharField(max_length=10)
    date_graded = models.DateTimeField(auto_now_add=True)

    is_english = models.BooleanField(default=False)
    is_maths = models.BooleanField(default=False)
    is_kiswahili = models.BooleanField(default=False)

    is_chemistry = models.BooleanField(default=False)
    is_physics = models.BooleanField(default=False)
    is_biology = models.BooleanField(default=False)

    is_geography = models.BooleanField(default=False)
    is_cre = models.BooleanField(default=False)
    is_history = models.BooleanField(default=False)

    is_computer_studies = models.BooleanField(default=False)
    is_business_studies = models.BooleanField(default=False)
    is_agriculture = models.BooleanField(default=False)

    # Function to calculate the grade
    def calculate_exam_grade(self):
        exam_marks = self.marks
        total_marks = ((exam_marks / 60) * 70)

        if total_marks >= 50:
            return 'A'
        
        elif total_marks >= 40:
            return 'B'
        
        elif total_marks >= 30:
            return 'C'
        
        elif total_marks >= 20:
            return 'D'
        
        elif total_marks >= 10:
            return 'E'
        
        else:
            return 'FAIL'

    def __str__(self):
        return f'{self.exam_name} with {self.marks} - {self.grade}'
    
    def save(self, *args, **kwargs):
        if not self.grade:
            self.grade = self.calculate_exam_grade()
        super().save(*args, **kwargs)

# Grade both cat and exam and roduce a common grade
class CatAndExam(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='cat_and_exam')
    stream_name = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='cat_and_exam')
    class_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat_and_exam')
    class_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='cat_and_exam')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='cat_and_exam')
    student_cat = models.IntegerField()
    student_exam = models.IntegerField()


    def __str__(self):
        return f'{self.class_student.student_code}: CAT: ({self.student_cat}) EXAM: ({self.student_exam}) '
    
# model to calculate both exam and cat
class CatAndExamGrading(models.Model):
    student_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat_and_exam_grading')
    student_code = models.CharField()
    student_subject = models.CharField(max_length=100)
    subject_cat_marks = models.IntegerField()
    subject_exam_marks = models.IntegerField()
    student_class = models.CharField(max_length=10)
    student_stream = models.CharField(max_length=10)
    subject_total = models.IntegerField()
    subject_grade = models.CharField(max_length=10)

    is_english_cat = models.IntegerField(default=0)
    is_english_exam = models.IntegerField(default=0)
    is_english_total = models.IntegerField(default=0)
    is_english_grade = models.CharField(default=0)

    is_maths_cat = models.IntegerField(default=0)
    is_maths_exam = models.IntegerField(default=0)
    is_maths_total = models.IntegerField(default=0)
    is_maths_grade = models.CharField(default=0)

    is_kiswahili_cat = models.IntegerField(default=0)
    is_kiswahili_exam = models.IntegerField(default=0)
    is_kiswahili_total = models.IntegerField(default=0)
    is_kiswahili_grade = models.CharField(default=0)

    is_physics_cat = models.IntegerField(default=0)
    is_physics_exam = models.IntegerField(default=0)
    is_physics_total = models.IntegerField(default=0)
    is_physics_grade = models.CharField(default=0)

    is_chemistry_cat = models.IntegerField(default=0)
    is_chemistry_exam = models.IntegerField(default=0)
    is_chemistry_total = models.IntegerField(default=0)
    is_chemistry_grade = models.CharField(default=0)

    is_biology_cat = models.IntegerField(default=0)
    is_biology_exam = models.IntegerField(default=0)
    is_biology_total = models.IntegerField(default=0)
    is_biology_grade = models.CharField(default=0)

    is_geography_cat = models.IntegerField(default=0)
    is_geography_exam = models.IntegerField(default=0)
    is_geography_total = models.IntegerField(default=0)
    is_geography_grade = models.CharField(default=0)

    is_cre_cat = models.IntegerField(default=0)
    is_cre_exam = models.IntegerField(default=0)
    is_cre_total = models.IntegerField(default=0)
    is_cre_grade = models.CharField(default=0)

    is_history_cat = models.IntegerField(default=0)
    is_history_exam = models.IntegerField(default=0)
    is_history_total = models.IntegerField(default=0)
    is_history_grade = models.CharField(default=0)

    is_agriculture_cat = models.IntegerField(default=0)
    is_agriculture_exam = models.IntegerField(default=0)
    is_agriculture_total = models.IntegerField(default=0)
    is_agriculture_grade = models.CharField(default=0)

    is_computer_studies_cat = models.IntegerField(default=0)
    is_computer_studies_exam = models.IntegerField(default=0)
    is_computer_studies_total = models.IntegerField(default=0)
    is_computer_studies_grade = models.CharField(default=0)

    is_business_studies_cat = models.IntegerField(default=0)
    is_business_studies_exam = models.IntegerField(default=0)
    is_business_studies_total = models.IntegerField(default=0)
    is_business_studies_grade = models.CharField(default=0)

    def __str__(self):
        return f'{self.student_code} in {self.student_class}{self.student_stream}'
    
# Calculate final student grade
class FinalGrade(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='final_grade')
    student = models.CharField(max_length=10)
    total_subjects = models.IntegerField()
    total_marks = models.IntegerField()
    final_grade = models.CharField()

    def __str__(self):
        return f'{self.student} ({self.final_grade})'

# report form model
class ReportForm(models.Model):
    class_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_forms')
    student_code = models.CharField(max_length=200)
    student_first_name = models.CharField(max_length=200)
    student_last_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=10)
    student_stream = models.CharField(max_length=10)
    student_average_grade = models.CharField(max_length=10)
    teacher_remarks = models.TextField()
    total_subjects = models.IntegerField()
    total_marks = models.IntegerField()
    term_name = models.CharField(max_length=20, unique=True)

    is_english_cat = models.IntegerField(default=0)
    is_english_exam = models.IntegerField(default=0)
    is_english_total = models.IntegerField(default=0)
    is_english_grade = models.CharField(default=0)

    is_maths_cat = models.IntegerField(default=0)
    is_maths_exam = models.IntegerField(default=0)
    is_maths_total = models.IntegerField(default=0)
    is_maths_grade = models.CharField(default=0)

    is_kiswahili_cat = models.IntegerField(default=0)
    is_kiswahili_exam = models.IntegerField(default=0)
    is_kiswahili_total = models.IntegerField(default=0)
    is_kiswahili_grade = models.CharField(default=0)

    is_physics_cat = models.IntegerField(default=0)
    is_physics_exam = models.IntegerField(default=0)
    is_physics_total = models.IntegerField(default=0)
    is_physics_grade = models.CharField(default=0)

    is_chemistry_cat = models.IntegerField(default=0)
    is_chemistry_exam = models.IntegerField(default=0)
    is_chemistry_total = models.IntegerField(default=0)
    is_chemistry_grade = models.CharField(default=0)

    is_biology_cat = models.IntegerField(default=0)
    is_biology_exam = models.IntegerField(default=0)
    is_biology_total = models.IntegerField(default=0)
    is_biology_grade = models.CharField(default=0)

    is_geography_cat = models.IntegerField(default=0)
    is_geography_exam = models.IntegerField(default=0)
    is_geography_total = models.IntegerField(default=0)
    is_geography_grade = models.CharField(default=0)

    is_cre_cat = models.IntegerField(default=0)
    is_cre_exam = models.IntegerField(default=0)
    is_cre_total = models.IntegerField(default=0)
    is_cre_grade = models.CharField(default=0)

    is_history_cat = models.IntegerField(default=0)
    is_history_exam = models.IntegerField(default=0)
    is_history_total = models.IntegerField(default=0)
    is_history_grade = models.CharField(default=0)

    is_agriculture_cat = models.IntegerField(default=0)
    is_agriculture_exam = models.IntegerField(default=0)
    is_agriculture_total = models.IntegerField(default=0)
    is_agriculture_grade = models.CharField(default=0)

    is_computer_studies_cat = models.IntegerField(default=0)
    is_computer_studies_exam = models.IntegerField(default=0)
    is_computer_studies_total = models.IntegerField(default=0)
    is_computer_studies_grade = models.CharField(default=0)

    is_business_studies_cat = models.IntegerField(default=0)
    is_business_studies_exam = models.IntegerField(default=0)
    is_business_studies_total = models.IntegerField(default=0)
    is_business_studies_grade = models.CharField(default=0)

    def __str__(self):
        return f'{self.student_first_name} {self.student_last_name} - {self.student_average_grade}'
