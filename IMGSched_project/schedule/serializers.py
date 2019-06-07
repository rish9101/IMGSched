from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from schedule.models import Users, MeetingsTable, CommentsTable, User

class UserDemoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['email'],
                validated_data['password'])
        return user

    class Meta:
        Model = User
        fields = ('id', 'username', 'email', 'password')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ( 'name', 'email', 'admin')

    def create(self, validated_data):

        return Users.objects.create(**validated_data)

class MeetingsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingsTable
        fields = ('id', 'meeting_date_time', 'purpose' , 'scheduler_id', 'people_invited')

    def create(self, validated_data):
        return MeetingsTable.objects.create(**validated_data)

    def update(delf, instance, validated_data):
        instance.meeting_date_time = validated_data.get('meeting_date_time', instance.meeting_date_time)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.people_invited = validated_data.get('people_invited', instance.people_invited)
