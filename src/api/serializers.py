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
        
class StructureFilterListeSerializer(serializers.ModelSerializer):
    structure_name = serializers.CharField(source='name')
    structure_type_name = serializers.CharField(source='type.name')

    class Meta:
        model = Structure
        fields = ['id', 'structure_name', 'structure_type_name']

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


class RecipientFilterListSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    town = serializers.SerializerMethodField()
    situation = serializers.SerializerMethodField()
    need = serializers.SerializerMethodField()

    class Meta:
        model = Recipient
        fields = [
            'id',
            'first_name',
            'last_name',
            'birthyear',
            'genre',
            'street',
            'town',
            'situation',
            'need',
        ]

    def get_genre(self, obj):
        return obj.genre.name if obj.genre else None

    def get_street(self, obj):
        return obj.street.name if obj.street else None

    def get_town(self, obj):
        return obj.street.town.name if obj.street and obj.street.town else None

    def get_situation(self, obj):
        return obj.situation.description if obj.situation else None

    def get_need(self, obj):
        return obj.need.description if obj.need else None


class WorkshopSerializer(serializers.ModelSerializer):
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all())

    class Meta:
        model = Workshop
        fields = '__all__'


#Cheques _____ ____ ___ __ _

class ChequeSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=Recipient.objects.all(), allow_null=True)
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all(), allow_null=True)
    workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), allow_null=True)

    class Meta:
        model = Cheque
        fields = '__all__'
        read_only_fields = ['created_at', 'number']


class ChequeGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = ['number', 'created_at']
        
        
class ChequeFilterListeSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    class Meta:
        model = Cheque
        fields = ['id', 'number', 'first_name', 'last_name', 'created_at', 'distribution_at', 'used_at']
    def get_first_name(self, obj):
        return obj.recipient.first_name if obj.recipient else None
    def get_last_name(self, obj):
        return obj.recipient.last_name if obj.recipient else None

# Users _____ ____ ___ __ _

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