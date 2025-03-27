from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdmin, IsDistributor, IsReceptor
from datetime import datetime
from django.utils import timezone

from .models import (
    StructureType, Structure, Agent, Role, Need, Situation, Town, Street, Genre, 
    Recipient, Workshop, Cheque
)

from .serializers import (
    StructureTypeSerializer, StructureSerializer, RoleSerializer, NeedSerializer, 
    SituationSerializer, TownSerializer, StreetSerializer, GenreSerializer, 
    RecipientSerializer, WorkshopSerializer, ChequeSerializer, ChequeGeneratorSerializer, AgentSerializer, RegisterSerializer, LoginSerializer
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
    permission_classes = [permissions.AllowAny]

class NeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [permissions.AllowAny]

# SITUATION
class SituationListCreateView(generics.ListCreateAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.AllowAny]

class SituationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.AllowAny]

# TOWN
class TownListCreateView(generics.ListCreateAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]

class TownDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]

# STREET
class StreetListCreateView(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.AllowAny]

class StreetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.AllowAny]

# GENRE
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

# STRUCTURE TYPE
class StructureTypeListCreateView(generics.ListCreateAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    permission_classes = [permissions.AllowAny]

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

# CHEQUE
class ChequeListCreateView(generics.ListCreateAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]

class ChequeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]
    
    
class ChequesGenerator(APIView):
    #permission_classes = [permissions.IsAuthenticated, IsAdmin]
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            count = request.query_params.get("count")
            if count is None:
                return Response({"error": "Le paramètre 'count' est requis."},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                count = int(count)
                if count < 1:
                    raise ValueError
            except ValueError:
                return Response({"error": "Le paramètre 'count' doit être un nombre entier positif."},
                                status=status.HTTP_400_BAD_REQUEST)
            numbers = self.generate_numbers(count)
            date_obj = datetime.now().date()
            cheques = [Cheque(number=number, created_at=date_obj) for number in numbers]
            Cheque.objects.bulk_create(cheques)
            queryset = Cheque.objects.filter(number__in=numbers)
            serializer = ChequeGeneratorSerializer(cheques, many=True)
            return Response({"message": f"{count} chèques générés avec succès!", "cheques": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
    def generate_numbers(self, count : int):
        numbers = set()
        date = datetime.now()
        year = date.year
        month = date.month
        day =date.day
        sufix = f"{year}{str(month).zfill(2)}{str(day).zfill(2)}"#exemple 20250101
        index = 0
        while(len(numbers) < count):
            prefix = str(index).zfill(4)#exemple 0001
            number = int(f"{sufix}{prefix}") #exemple 202501010001
            if(not Cheque.objects.filter(number=number).exists()):
                numbers.add(number)
            index += 1
        return numbers
            

#USER
class RegisterView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

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