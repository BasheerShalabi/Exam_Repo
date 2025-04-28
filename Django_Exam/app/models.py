from django.db import models
import bcrypt
import re
from datetime import datetime
# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, postData):
        errors = {}
        if len(postData['email']) < 5:
            errors['email'] = "Email must be at least 5 characters"
        return errors
    def validate_register(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already in use"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match"
        return errors
    
class ProjectManager(models.Manager):
    def validate_project(self,postData):
        errors = {}
        datetime.strptime(postData['startdate'], "%Y-%m-%d").date()
        if len(postData['name']) < 3:
            errors['name'] = "Project name must be at least 3 characters"
        if len(postData['description']) < 10:
            errors['description'] = "Description must be at least 10 characters"
        if postData['startdate'] == '':
            errors['startdate'] = "Start date can not be empty"
        if postData['enddate'] == '':
            errors['enddate'] = "End date can not be empty"
        if not datetime.now().date() <= datetime.strptime(postData['startdate'], "%Y-%m-%d").date():
            errors['startdate'] = "Start Day can not be in the past"
        if not datetime.now().date() <= datetime.strptime(postData['enddate'], "%Y-%m-%d").date():
            errors['enddate'] = "End Day can not be in the past"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def get_user_by_id(id):
        return User.objects.get(id=id)
    
    def register_user(first_name, last_name, email, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
        return user

    def login_user(email, password):
        user = User.objects.filter(email=email)
        if not user:
            return None
        if bcrypt.checkpw(password.encode(), user[0].password.encode()):
            return user[0]
        else:
            return None

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User,related_name="my_projects",on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User,related_name="joined_projects")
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ProjectManager()

    def get_all_projects():
        return Project.objects.all()

    def get_project_by_id(id):
        return Project.objects.get(id=id)
    
    def create_project(post,user_id):
        name = post['name']
        description = post['description']
        owner = User.objects.get(id=user_id)
        startdate = post['startdate']
        enddate = post['enddate']
        project = Project.objects.create(name=name,description=description,owner=owner,startdate=startdate,enddate=enddate)
        return project
    
    def delete_project(project_id):
        project = Project.get_project_by_id(project_id)
        project.delete()
    
    def edit_project(post,project_id):
        project = Project.get_project_by_id(project_id)
        project.name = post['name']
        project.description = post['description']
        project.startdate = post['startdate']
        project.enddate = post['enddate']
        project.save()
    
    def join_project(project_id,user_id):
        project = Project.get_project_by_id(project_id)
        user = User.get_user_by_id(user_id)
        project.collaborators.add(user)
    
    def leave_project(project_id,user_id):
        project = Project.get_project_by_id(project_id)
        user = User.get_user_by_id(user_id)
        project.collaborators.remove(user)
    

