from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from web_app.models import (
    User, Todo, Post
)
from api.serializers import (
    LoginSerializer,
    TodoSerializer, PostSerializer
)
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,                        
            },
            'status' : 200,
            'message' : 'You are login right now...'
        })

class LogoutView(APIView):
    authenticate_classes = (TokenAuthentication, )
    
    def post(self, request):
        django_logout(request)
        return JsonResponse({'message' : 'You have been logout...'})

# Start Controller Todo
class TodoListApiView(APIView):    

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)

    def post(self, request, *args,**kwargs):
        data = {
            'title' : request.data.get('title'),
            'completed' : request.data.get('completed'),            
        }
        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class TodoDetailApiView(APIView):

    def get_object(self, id):
        try:
            return Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        todo_instance = self.get_object(id)
        if not todo_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST 
            )

        serializer = TodoSerializer(todo_instance)
        response = {
            'status' : status.HTTP_200_OK, 
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data 
        }
        return Response(response, status = status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        todo_instance = self.get_object(id)
        if not todo_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'title' : request.data.get('title'),
            'completed' : request.data.get('completed'),            
        }
        serializer = TodoSerializer(instance = todo_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
       
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        todo_instance = self.get_object(id)
        if not todo_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
                    
        todo_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)
# End Controller Todo

# Start Controller Post
class PostListApiView(APIView):    

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)

    def post(self, request, *args,**kwargs):
        data = {
            'title' : request.data.get('title'),
            'body' : request.data.get('body'),            
        }
        serializer = PostSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class PostDetailApiView(APIView):

    def get_object(self, id):
        try:
            return Post.objects.get(id = id)
        except Post.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        post_instance = self.get_object(id)
        if not post_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST 
            )

        serializer = PostSerializer(post_instance)
        response = {
            'status' : status.HTTP_200_OK, 
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data 
        }
        return Response(response, status = status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        post_instance = self.get_object(id)
        if not post_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'title' : request.data.get('title'),
            'body' : request.data.get('body'),            
        }
        serializer = PostSerializer(instance = post_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
       
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        post_instance = self.get_object(id)
        if not post_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
                    
        post_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)
# End Controller Post

