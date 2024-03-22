from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Movie,MovieList,Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse,HttpResponse
from .utils import *
import re
import uuid



# Create your views here.
@login_required(login_url='login')
def index(request):
     movies = Movie.objects.all()
     featured_movie = movies[len(movies)-1]
     
     context = {
          'movies':movies,
          'featured_movie':featured_movie
     }
     return render(request , 'index.html', context)


@login_required(login_url='login')
def movie(request,pk):
     movie_uuid = pk
     movie_details = Movie.objects.get(uu_id=movie_uuid)
     
     context = {
          'movie_details':movie_details
     }
     
     return render(request, 'movie.html',context)

@login_required(login_url='login')
def genere(request,pk):
     movie_genre = pk
     movies = Movie.objects.filter(genere=movie_genre)
     context = {
          'movies':movies,
          'movie_genre':movie_genre
     }
     return render(request, 'general.html' , context)

@login_required(login_url='login')
def search(request):
     if request.method == 'POST':
          search_term = request.POST['search_term']
          # title__icontains search by title given in search_term
          movies = Movie.objects.filter(title__icontains=search_term)
          
          context = {
               'movies':movies,
               'search_term':search_term
          }
          return render(request, 'search.html' , context)
     else:
          return redirect('/')

@login_required(login_url='login')
def my_list(request):
     movie_list = MovieList.objects.filter(owner_user=request.user)
     user_movie_list=[]
     
     # getting only the movie form movie_list
     for movie in movie_list:
          user_movie_list.append(movie.movie)
          
     context = {
          'movies':user_movie_list
     }
     return render(request, 'my_list.html' , context)

@login_required(login_url='login')
def add_to_list(request):
     if request.method == 'POST':
          movie_url_id = request.POST.get('movie_id')

          # Search the UUID pattern in the movie URL
          uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
          match = re.search(uuid_pattern, movie_url_id)

          # Check if UUID pattern is found in the movie URL
          if match:
               movie_id = match.group()
               movie = get_object_or_404(Movie, uu_id=movie_id)
               movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

               if created:
                    response_data = {'status': 'success', 'message': 'Added'}
               else:
                    response_data = {'status': 'info', 'message': 'Movie already in the list'}
          else:
               response_data = {'status': 'error', 'message': 'Invalid movie ID format'}
               return JsonResponse(response_data, status=400)

          return JsonResponse(response_data)
     else:
          return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
          
          
def signin(request):
     if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          
          try:
               user_obj = User.objects.filter(username = username).first()
               if user_obj is None:
                    messages.info(request , 'User does not Exist')
                    return redirect('login')
               
               profile_obj = Profile.objects.filter(user =  user_obj).first()
               if not profile_obj.is_verified:
                    messages.info(request, 'Not verified Please check your mail')
                    return redirect('login')
               else:
                    user = authenticate(username=username , password=password)
                    if user is None:
                         messages.info(request, 'Password is Incorrect')
                         return redirect('login')
                    
                    login(request , user)
                    return redirect('/')
          except Exception as e:
               messages.info(request , 'Profile does not exist')
               return redirect('error')
     return render(request , 'login.html')

def signup(request):
     if request.method == 'POST':
          email = request.POST['email']
          username = request.POST['username']
          password = request.POST['password']
          password2 = request.POST['password2']
          
          if password == password2:
               if User.objects.filter(email=email).exists():
                    messages.info(request ,'Email already exists')
                    return redirect('signup')
               elif User.objects.filter(username=username).exists():
                    messages.info(request,'Username already exists')
                    return redirect('signup')
               else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    
                    # create Profile
                    auth_token = str(uuid.uuid4())
                    profile_obj = Profile.objects.create(
                              user = user,
                              email_token = auth_token
                              )
                    profile_obj.save()
                              
                    send_email_token(email , auth_token)
                    return redirect('token_send')
          else:
               messages.info(request , 'Check your Password again')
               return redirect('signup')
     else:
          pass
     return render(request , 'signup.html')

def token_send(request):
     return render(request, 'token_send.html')

def success(request):
     return render(request , 'success.html')

def error(request):
     return render(request, 'error.html')

def verify(request , token):
     try:
          profile_obj = Profile.objects.filter(email_token = token).first()
          if profile_obj:
               if profile_obj.is_verified:
                    messages.success(request, 'Your account has already been Verified')
                    return redirect('login')
               else:
                    profile_obj.is_verified = True
                    profile_obj.save()
                    messages.success(request , 'Your account has been Verified' )
                    return redirect('login')
          else:
               return redirect('error')
     except Exception as e:
          return redirect('error')
          
def forget_password(request):
     try:
          if request.method == 'POST':
               username = request.POST.get('username')
               
               if not User.objects.filter(username=username).first():
                    messages.success(request, 'Username is not Found')
                    return redirect('forget-password')
               
               user_obj = User.objects.get(username = username)
               token = str(uuid.uuid4())
               profile_obj = Profile.objects.get(user = user_obj)
               profile_obj.forget_password_token = token
               profile_obj.save()
               send_forget_password_mail(user_obj.email, token)
               messages.success(request, 'Mail is sent to your email address')
               return redirect('forget-password')
     except Exception as e:
          pass        
     return render(request, 'forget_password.html')

def change_password(request, token):
     context = {}
     try:
          profile_obj = Profile.objects.filter(forget_password_token = token).first()
          context = {
               'user_id': profile_obj.user.id
          }
          
          if request.method == "POST":
               new_password = request.POST.get('password')
               confirm_password = request.POST.get('password1')
               user_id = request.POST.get('user_id')
               
               if user_id is None:
                    messages.info(request, 'User id is Not Found')
                    return redirect(f'/change-password/{token}/')
               
               if new_password != confirm_password:
                    messages.info(request, 'Please re-check your password')
                    return redirect(f'/change-password/{token}/')
                    
               user_obj = User.objects.get(id = user_id)
               user_obj.set_password(new_password)
               user_obj.save()
               messages.info(request, 'Password Changed Successfully')
               return redirect('login')
                    
     except Exception as e:
          pass
     
     return render(request, 'change_password.html' , context)

@login_required(login_url='login')
def logout_usr(request):
     logout(request)
     return redirect('login')