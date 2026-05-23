from django.urls import path
from FonoAppNoticias import views

urlpatterns = [
    # -------------------------------------------------------------------------
    # MÉTODO: GET
    # URL: /api/noticias/listar/
    # HEADERS: Ninguno (Acceso público)
    # BODY: Ninguno
    # RESPUESTA ESPERADA: Un arreglo JSON con todas las noticias y sus imágenes.
    # [
    #   {
    #     "id_noticia": 1,
    #     "titulo": "Campaña de vacunación gratuita",
    #     "contenido": "Este fin de semana estaremos realizando...",
    #     "fecha_creacion": "2026-05-23T10:00:00Z",
    #     "FonoApp_Administracion": 1,
    #     "imagenes": [ 
    #        { "id": 1, "imagen": "/media/noticias/imagenes/foto1.jpg", "fecha_subida": "..." } 
    #     ]
    #   }
    # ]
    # -------------------------------------------------------------------------
    path('listar/', views.noticias_listar, name='noticias-listar'),

    # -------------------------------------------------------------------------
    # MÉTODO: POST
    # URL: /api/noticias/crear/
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY (IMPORTANTE): Como recibe imágenes, DEBE ser un objeto "FormData" (multipart/form-data), NO un JSON.
    # EN EL FRONTEND (Astro/JS):
    #   const formData = new FormData();
    #   formData.append('titulo', 'Nuevo título de noticia');
    #   formData.append('contenido', 'Cuerpo de la noticia...');
    #   formData.append('imagenes_subidas', archivoFile1); // Opcional, hasta 4 archivos
    # RESPUESTA ESPERADA: El objeto JSON de la noticia recién creada (Status 201).
    # -------------------------------------------------------------------------
    path('crear/', views.noticias_crear, name='noticias-crear'),

    # -------------------------------------------------------------------------
    # MÉTODO: DELETE
    # URL: /api/noticias/1/eliminar/  <-- Reemplazar '1' por el ID de la noticia
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY: Ninguno
    # RESPUESTA ESPERADA (JSON):
    # {
    #   "mensaje": "Noticia eliminada correctamente"
    # }
    # -------------------------------------------------------------------------
    path('<int:id_noticia>/eliminar/', views.noticia_eliminar, name='noticia-eliminar'),
]