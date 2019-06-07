from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import User, Users, MeetingsTable, CommentsTable
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from schedule.serializers import UserDemoSerializer, UsersSerializer, MeetingsTableSerializer
from datetime import datetime
from django.utils import timezone
import pytz
# Create your views here.


def home(request):
    user = request.user
    if request.method=='GET' and user.is_authenticated:
        email = user.email
        User2 = Users.objects.get(email=email)
        serializer = UsersSerializer(User2)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("please login first")

def register(request):
    if request.method=='GET':
        return HttpResponse("Please register first")

class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserDemoSerialzier(data=request.data)
        serializer_data = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user2 = serializer_data.save()
            if user and user2:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def schedule_list(request):
    
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            meetings_invited_in = []
            user = Users.objects.get(email=user.email)
            if user.admin==1:
                meetings = MeetingsTable.objects.filter(meeting_date_time__gte=datetime.now())
            else:
                all_meetings = MeetingsTable.objects.all()
                for meet in all_meetings:
                    if email == meet.scheduler_id.email:
                        meetings_invited_in.append(meet.id)
                    else:
                        invited_people = meet.people_invited.all()
                        for person in invited_people:
                            if email == person.email:
                                meetings_invited_in.append(meet.id)
                meetings = MeetingsTable.objects.filter(meeting_date_time__gte=timezone.now()).filter(id__in=meetings_invited_in)
            serializer = MeetingsTableSerializer(meetings, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = MeetingsTableSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Jsonresponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def meeting_detail(request, pk):
    user = request.user
    if user.is_authenticated():
        try:
            meeting = MeetingsTable.object.get(id=pk)
            user = Users.objects.get(email=user.email)
        except MeetingsTable.DoesNotExist and Users.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = MeetingsTableSerializer(meeting)
            return Jsonresponse(serializer.data)

        elif request.method == 'DELETE':
            if user.admin==1 or user.email==meeting.scheduler_id:
                meeting.delete()
                return HttpResponse(status=204)
            else:
                return HttpResponse("You are not authorized to delete this meeting")

        elif request.method == 'PUT':
            if user.admin==1 or user.email==meeting.scheduler_id:
                data = JSONParser().parse(request)
                serializer = MeetingsTableSerializer(meetings, data=data)
                if serializer.is_valid():
                    return Jsonresponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)
            else:
                return HttpResponse("You are not authorized to change this meetings details")
