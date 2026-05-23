from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from FonoAppNoticias.models import FonoApp_Noticias
from FonoAppNoticias.serializer import FonoApp_NoticiasSerializer
from FonoAppFunciones.authentication import CustomJWTAuthentication

@api_view(['GET'])
@permission_classes([AllowAny]) # Lo dejo público para que cualquiera pueda leer las noticias, cámbialo a IsAuthenticated si es privado
def noticias_listar(request):
    """
    Lista todas las noticias activas con sus imágenes.
    Aprovecha el select_related y prefetch_related para máxima velocidad.
    """
    noticias = FonoApp_Noticias.objects.activas().con_detalles()
    serializer = FonoApp_NoticiasSerializer(noticias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def noticias_crear(request):
    """
    Crea una noticia nueva y asocia las imágenes subidas.
    """
    # ¡MUY IMPORTANTE! Pasamos el context={'request': request} 
    # para que el Serializer pueda sacar el usuario del token.
    serializer = FonoApp_NoticiasSerializer(
        data=request.data, 
        context={'request': request} 
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def noticia_eliminar(request, id_noticia):
    """
    Realiza un borrado lógico de la noticia.
    """
    actualizado = FonoApp_Noticias.objects.eliminar_logico(id_noticia)
    
    if actualizado:
        return Response({'mensaje': 'Noticia eliminada correctamente'}, status=status.HTTP_200_OK)
        
    return Response({'error': 'Noticia no encontrada o ya eliminada'}, status=status.HTTP_404_NOT_FOUND)