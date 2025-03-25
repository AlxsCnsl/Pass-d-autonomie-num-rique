from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .permissions import IsAdmin, IsDistributor, IsReceptor

from .models import (
    StructureType, Structure, Agent, Role, Need, Situation, Town, Street, Genre, 
    Recipient, Workshop, Cheque
)

from .serializers import (
    StructureTypeSerializer, StructureSerializer, RoleSerializer, NeedSerializer, 
    SituationSerializer, TownSerializer, StreetSerializer, GenreSerializer, 
    RecipientSerializer, WorkshopSerializer, ChequeSerializer, AgentSerializer, RegisterSerializer, LoginSerializer
)

import logging
logger = logging.getLogger(__name__)

# ROLE
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# NEED
class NeedListCreateView(generics.ListCreateAPIView):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class NeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [permissions.AllowAny]

# SITUATION
class SituationListCreateView(generics.ListCreateAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class SituationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.AllowAny]

# TOWN
class TownListCreateView(generics.ListCreateAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class TownDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]

# STREET
class StreetListCreateView(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class StreetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.AllowAny]

# GENRE
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

# STRUCTURE TYPE
class StructureTypeListCreateView(generics.ListCreateAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class StructureTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    permission_classes = [permissions.AllowAny]

# STRUCTURE
class StructureListCreateView(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class StructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.AllowAny]

# RECIPIENT
class RecipientListCreateView(generics.ListCreateAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['birthyear']
    search_fields = ['first_name', 'last_name']

class RecipientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [permissions.AllowAny]

# WORKSHOP
class WorkshopListCreateView(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

# CHEQUE (Sécurisé, seul un admin peut créer un chèque)
class ChequeListCreateView(generics.ListCreateAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ChequeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]


#USER
class RegisterView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]




class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Appel à la méthode post de TokenObtainPairView pour obtenir le token
        response = super().post(request, *args, **kwargs)

        # Vérifier que response.data est un dictionnaire mutable
        response_data = response.data.copy() if isinstance(response.data, dict) else {}

        # Sérialiser les données reçues
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # L'utilisateur authentifié est directement l'instance d'Agent (si l'authentification a réussi)
        user = serializer.validated_data['user']  # Utilisation de 'user' pour accéder à l'utilisateur

        logger.info(f"Utilisateur authentifié: {user}")

        # Vérifier que l'utilisateur est bien un Agent
        if isinstance(user, Agent):
            logger.info(f"Utilisateur est un Agent: {user.username}")

            # Sérialiser les informations de l'agent
            agent_serializer = AgentSerializer(user)
            response_data["user"] = agent_serializer.data
        else:
            logger.warning(f"L'utilisateur n'est pas un agent ou non authentifié.")
            response_data["user"] = None

        # Retourner la réponse finale avec les données supplémentaires
        return Response(response_data)


class AgentListView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
@api_view(['POST'])
def logout_view(request):
    """Déconnexion en blacklistant le token"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)