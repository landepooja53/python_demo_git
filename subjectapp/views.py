from rest_framework.decorators import api_view
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Subject 
from .serializers import SubjectSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import Subject
from .forms import SubjectForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


#DRF handles all API operations automatically so you don’t have to write GET/POST manually.
#SubjectViewSet is a DRF (Django REST Framework) class-based view 
class SubjectViewSet(viewsets.ModelViewSet):  #ModelViewSet automatically provides CRUD APIs for a model:
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer   #serializer_class tells how to convert Python objects to JSON


# Login
@csrf_exempt
def subject_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('subject_list')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'subject_login.html')

@login_required
def subject_list_view(request):
    subjects = Subject.objects.all()
    for idx,subject in enumerate(subjects,start=1):
        subject.sr_no=idx
    
    return render(request, 'subject_list.html', {'subjects': subjects})

# Delete
@login_required
def delete_subject_view(request, pk):
    subject = Subject.objects.get(id=pk)
    subject.delete()
    return redirect('subject_list')


@login_required 
def subject_logout_view(request):
    logout(request)
    return redirect('subject_login')


@csrf_exempt
def subject_signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'subject_signup.html')

        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        return redirect('subject_login')

    return render(request, 'subject_signup.html')



@csrf_exempt
@api_view(['GET'])
def subject_list_api(request):
    subjects=Subject.objects.all()
    serializer=SubjectSerializer(subjects,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def add_subject_api(request):
    serializer=SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def subject_detail_api(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

   
    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Add
@csrf_exempt
@login_required
def add_subject_view(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})

# Edit
@login_required
def edit_subject_view(request, pk):
    subject = Subject.objects.get(id=pk)  
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)  
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)  
    return render(request, 'edit_subject.html', {'form': form, 'subject': subject})


