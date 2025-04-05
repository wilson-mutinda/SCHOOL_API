from django.db import models
from django.utils import timezone

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

# student model
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='students')
    parent_code = models.CharField(max_length=100, unique=True)
    parent_email = models.EmailField(unique=True)
    student_code = models.CharField(max_length=100, unique=True)

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
