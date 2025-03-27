from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    StructureType, Structure, Agent, Role, Need, Situation, Town, Street, Genre, 
    Recipient, Workshop, Cheque
)

class StructureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureType
        fields = '__all__'

class StructureSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=StructureType.objects.all())

    class Meta:
        model = Structure
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = '__all__'

class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'

class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = '__all__'

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class RecipientSerializer(serializers.ModelSerializer):
    town = serializers.PrimaryKeyRelatedField(queryset=Town.objects.all())
    street = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    need = serializers.PrimaryKeyRelatedField(queryset=Need.objects.all(), allow_null=True)
    situation = serializers.PrimaryKeyRelatedField(queryset=Situation.objects.all(), allow_null=True)

    class Meta:
        model = Recipient
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class WorkshopSerializer(serializers.ModelSerializer):
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all())

    class Meta:
        model = Workshop
        fields = '__all__'

class ChequeSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=Recipient.objects.all(), allow_null=True)
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all(), allow_null=True)
    workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), allow_null=True)

    class Meta:
        model = Cheque
        fields = ['user_id', 'structure', 'workshop', 'distribution_at', 'used_at' ]
        read_only_fields = ['created_at', 'number']

class ChequeGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = ['number', 'created_at']

# User 

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Agent, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class AgentSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    class Meta:
        model = Agent
        fields = ['id', 'username', 'role', 'structure']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    class Meta:
        model = Agent
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = Agent.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role 
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        data['user'] = user
        return data