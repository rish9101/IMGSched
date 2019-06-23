from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import User, MeetingsTable, CommentsTable
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from schedule.serializers import UserSerializer, MeetingsTableSerializer
from datetime import datetime
from django.utils import timezone
import pytz
# Create your views here.


def home(request):
    return render(request, 'home.html')
    #user = request.user
    #if request.method=='GET' and user.is_authenticated:
        #User2 = Users.objects.get(email=email)
        #serializer = UsersSerializer(User2)
        #return JsonResponse(user.email, safe=False)
    #else:
        #return HttpResponse("please login first")

def register(request, *args, **kwargs):
    if request.method=='GET':
        return HttpResponse("Please register first")


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerialzier(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = MeetingsTable.objects.all()
    serializer_class = MeetingsTableSerializer
    
    def get_permission(self):
        views = ['list', 'create', 'retrieve', 'partial_update', 'delete']

        if self.action in views:
            permission_classes = [IsAuthenticated]
        else:
            permisiion_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


    def list(self, request):
        user = request.user
        meetings_invited_in =[]
        if user.admin:
            meetings = MeetingsTable.objects.filter(meetin_date_time__gte=timezone.now())
        else:
            all_meetings = MeetingsTable.objects.all()
            for meet in all_meetings:
                if user.email == meet.scheduler_id.email:
                    meetings_invited_in.append(meet.id)
                else:
                    invited_people = meet.people_invited.all()
                    for person in invited_people:
                        if email == person.email:
                            meetings_invited_in.append(meet.id)
            meetings = MeetingsTable.objects.filter(meeting_date_time__gte=timezone.now()).filter(id__in=meetings_invited_in)
        serializer = Meetingstableserializer(meetings.data, many=True)

        return Response(serializer.data)

    def create(self, request):
        pass


    def retrieve(self, request, pk=None):
        pass
        
    def partial_update(self, request, pk=None):
        meeting = MeetingTable.objects.get(id=pk)
        user = request.user

        if user.admin or user.email == meeting.scheduler_id:
            data = JSONParser.parse().request
            serializer = MeetingsTableSerializer(meeting, data=data)
            if serializer.is_valid:
                serializer.update
                return Response(serializer.data)
            else:
                return Response("Wrong data sent")
        else:
            return Response("You aren't authorized to make changes to this meeting")
    
    def delete(self, request, pk=None):
        pass
