from django.shortcuts import render,redirect
from .models import User , Project
from django.contrib import messages
from datetime import datetime 
# Create your views here.

def index(request):
    if not 'user' in request.session:
        return render(request, 'index.html')
    else:
        user = request.session['user']
        return redirect('/dashboard')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_register(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.register_user(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'])
            request.session['user'] = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
                
            return redirect('/dashboard')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.login_user(request.POST['email'], request.POST['password'])
            if user:
                request.session['user'] = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid email or password")
                return redirect('/')
    else:
        return redirect('/')

def logout(request):
    if 'user' in request.session:
        request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user' in request.session:
        context = {
            'user': User.get_user_by_id(request.session['user']['id']),
            'projects': Project.get_all_projects()
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def create_project(request):
    if 'user' in request.session:
        if request.method == 'POST':
            errors = Project.objects.validate_project(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/create_project')
            else:
                project = Project.create_project(request.POST,request.session['user']['id'])
                return redirect(f'/project_info/{project.id}')
        else:
            context ={
                'today': datetime.now()
            }
            return render(request,'create_project.html',context)
    else:
        return redirect('/')

def project_info(request,project_id):
    if 'user' in request.session:
        context = {
            'user': User.get_user_by_id(request.session['user']['id']),
            'project': Project.get_project_by_id(project_id)
        }
        return render(request,'project_info.html',context)
    else:
        return redirect('/')

def edit_project(request,project_id):
    if 'user' in request.session:
        if request.method == 'POST':
            errors = Project.objects.validate_project(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/edit_project/{project_id}')
            else:
                Project.edit_project(request.POST,project_id)
                return redirect(f'/project_info/{project_id}')
        else:
            project = Project.get_project_by_id(project_id)
            if project.owner.id is request.session['user']['id']:
                context={
                'user': User.get_user_by_id(request.session['user']['id']),
                'project': project,
                'today': datetime.now()
                }
                return render(request,'edit_project.html',context)
            else:
                return redirect('/dashboard')
    else:
        return redirect('/')

def delete_project(request):
    if 'user' in request.session:
        if request.method == 'POST':
            Project.delete_project(request.POST['project_id'])
            return redirect('/dashboard')
    else:
        return redirect('/')

def join_project(request):
    if 'user' in request.session:
        if request.method == 'POST':
            Project.join_project(request.POST['project_id'],request.session['user']['id'])
            return redirect('/dashboard')
    else:
        return redirect('/')

def leave_project(request):
    if 'user' in request.session:
        if request.method == 'POST':
            Project.leave_project(request.POST['project_id'],request.POST['user_id'])
            return redirect('/dashboard')
    else:
        return redirect('/')