from .models import Userdata,ImagePost,Like
from rest_framework.decorators import api_view,parser_classes,permission_classes
from rest_framework.response import Response
from .serializers import userserializer,ImagePostSerializer,loginserializer,searchSerializer,profileserializer,postdataS
from rest_framework import status
from .models import CustomToken
from .authentication  import CustomTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes

from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse,HttpResponse
from rest_framework.parsers import MultiPartParser,FormParser
from django.contrib.auth import authenticate
from rest_framework.views import APIView
#from myapp.models import CustomToken
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import uuid
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import  permission_classes



#from django.contrib.auth.models import Userdata



def delete_user_by_email(username):
    try:
        # Locate the user by email
        user = Userdata.objects.filter(username=username)

        if user.exists():
            user.delete()
            return f"User with email {email} has been deleted."
        else:
            return f"No user found with email {email}."
    except Exception as e:
        return f"An error occurred: {e}"

delete_user_by_email('mahesh')


@api_view(['POST','OPTIONS'])
def home(request):
    if request.method=='POST':
        a=request.data['password']
        request.data['password']=make_password(a)
        serializer=userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            datas={"message":"message suucessfully created"}
            return Response (datas)
        return Response({"message":"somthing worng errors occur"})
        
def myself(request):
     obj=Userdata.objects.all()
     serializer=userserializer(obj,many=True)

     return HttpResponse(serializer.data)




@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
class imageupload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImagePostSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method=='GET':
        data=request.user
    


        serializer=profileserializer(data, context={'request':request})
        print(serializer.data)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def postdata(request):
    if request.method=='GET':
        data=request.user
    

        post=ImagePost.objects.filter(user=data)
        print(post)
        
        serializer=postdataS(post,many=True , context={'request':request})
        print(serializer.data)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request):
    if request.method=='POST':
        post_id=request.data['post_id']
        print(post_id)
        post = ImagePost.objects.get(id=post_id)
        user=request.user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            post = get_object_or_404(ImagePost, id=post_id)
            post.totallikes += 1
            post.save()
            print(post.totallikes)
        return JsonResponse({"message":"message sucessfully created"})
    return JsonResponse({"message":"message sucessfully created"})        



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request):
    post_id = request.data.get('post_id')
    try:
        post = ImagePost.objects.get(id=post_id)
    except ImagePost.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        post = get_object_or_404(ImagePost, id=post_id)
        post.totallikes -= 1
        post.save()
        return JsonResponse({'message': 'Post unliked successfully'}, status=200)
    except Like.DoesNotExist:
        return JsonResponse({'error': 'You have not liked this post'}, status=400)

        

    




@api_view(['POST'])
@permission_classes([AllowAny]) 
def search(request):
    if request.method=='POST' and request.user.is_authenticated:
        data=request.data['query']
        image=ImagePost.objects.select_related('user') \
                            .filter(title__icontains=data)

        serializer=searchSerializer(image, context={'request':request},many=True)
        print(serializer.data)
        return Response(serializer.data)
    else:
        data=request.data['query']
        image=ImagePost.objects.filter(title__icontains=data)
        serializer=searchSerializer(image, context={'request':request},many=True)
        print(serializer.data)
        return Response(serializer.data)

    
        




class loginapi(APIView):
    def post(self,request):
        data=request.data
        serializer=loginserializer(data=data)
    
        if  serializer.is_valid():
            
             email=serializer.data['email']
             password=serializer.data['password']
            
             user=authenticate(request,email=email,password=password)
             print(user)
        
        
        if user is not None:
            user = Userdata.objects.get(username=user)
            print(user)

            token,created= CustomToken.objects.get_or_create(user=user)
            print(token)
           
            return Response({
                "status":True,
               'token':token.key
               
            })
        else:
            return Response({
            "status":False,
            "data":{},
            "message":"Invalid credentials"
               })