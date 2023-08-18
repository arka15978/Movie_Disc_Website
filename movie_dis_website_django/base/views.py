from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Movie, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm




def signinScreen(request):
    
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        
        
        

        try:
            user = User.objects.get(email=email)
            login(request,user)

        except:
            messages.error(request, 'User does not exist')

        return redirect('home-page')
        

        
    context = {'page': 'login'}
    return render(request, 'base/login_signup.html', context)


def signout(request):
    logout(request)
    return redirect('home-page')


def signUpScreen(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        print(request.POST)
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('home-page')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_signup.html', {'form': form})


def homePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(movie__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    movies = Movie.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'movies': movies,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/homePage.html', context)


def roomPage(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room-page', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/roomPage.html', context)


def userProfileView(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    movies = Movie.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'movies': movies}
    return render(request, 'base/user-profile.html', context)


@login_required(login_url='signin')
def createRoom(request):
    form = RoomForm()
    movies = Movie.objects.all()
    if request.method == 'POST':
        movie_name = request.POST.get('movie')
        movie, created = Movie.objects.get_or_create(name=movie_name)

        Room.objects.create(
            host=request.user,
            movie=movie,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home-page')

    context = {'form': form, 'movies': movies}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    movies = Movie.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        movie_name = request.POST.get('movie')
        movie, created = Movie.objects.get_or_create(name=movie_name)
        room.name = request.POST.get('name')
        room.movie = movie
        room.description = request.POST.get('description')
        room.save()
        return redirect('home-page')

    context = {'form': form, 'movies': movies, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home-page')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home-page')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/edit-user.html', {'form': form})


def moviesCard(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    movie_list = Movie.objects.filter(name__icontains=q)
    return render(request, 'base/movies.html', {'movies': movie_list})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
 