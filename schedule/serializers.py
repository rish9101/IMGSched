from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from schedule.models import User, MeetingsTable, CommentsTable

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    meetings_scheduled = serializers.PrimaryKeyRelatedField(many=True,
    queryset=MeetingsTable.objects.all())

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['email'],
                )
        return user

    class Meta:
        Model = User
        fields = ( 'email', 'password', 'meetings_scheduled')


class MeetingsTableSerializer(serializers.ModelSerializer):
    people_invited = UserSerializer(many=True)
    people_email = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            many = True, write_only=True)
    scheduler_id = serializers.PrimaryKeyRelatedField(
            read_only=False, queryset=User.objects.all())

    class Meta:
        model = MeetingsTable
        fields = ('id', 'meeting_date_time', 'purpose' , 'scheduler_id', 'people_invited', 'people_email')

    def create(self, validated_data):
        instance = super().create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.meeting_date_time = validated_data.get('meeting_date_time', instance.meeting_date_time)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.people_invited = validated_data.get('people_invited', instance.people_invited)
