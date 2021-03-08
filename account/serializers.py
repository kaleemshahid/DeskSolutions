from .models import User, Organization, Attendance, ComplaintBox
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', ]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['radius', 'longitude', 'latitude', ]


class AttendanceSerializer(serializers.ModelSerializer):

    # attendance_details = serializers.SerializerMethodField()

    # def get_attendance_details(self, obj):
    #     test = {
    #         "test" : obj.is_present,
    #     }
    #     return test


    class Meta:
        model = Attendance
        fields = ['user_profile', 'date', 'punch_in_time', 'punch_out_time', 'is_present']


class CreateComplaintBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintBox
        fields = '__all__'


class ListComplaintBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintBox
        fields = ['complain_date', 'subject', 'complain']
