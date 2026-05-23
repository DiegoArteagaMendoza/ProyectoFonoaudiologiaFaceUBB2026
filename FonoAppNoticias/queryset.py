from django.db import models

class FonoApp_Noticias_Queryset(models.QuerySet):
    
    def activas(self):
        """
        Retorna solo las noticias que no han sido eliminadas lógicamente.
        """
        return self.filter(estado=True)

    def con_detalles(self):
        """
        ¡Súper importante para el rendimiento! 
        Optimiza la consulta usando select_related (para traer los datos del usuario)
        y prefetch_related (para traer las imágenes). Evita el problema N+1.
        """
        return self.select_related('FonoApp_Administracion').prefetch_related('imagenes')

    def eliminar_logico(self, id_noticia):
        """
        Oculta la noticia sin borrarla de la base de datos.
        """
        filas_actualizadas = self.filter(id_noticia=id_noticia).update(estado=False)
        return filas_actualizadas > 0

    def crear_noticia(self, usuario, titulo, contenido, imagenes=None, **extra_fields):
        """
        Crea la noticia y asocia las imágenes (si las hay).
        Se asegura de que no se superen las 4 imágenes.
        """
        # 1. Validar el límite de imágenes antes de crear nada
        if imagenes and len(imagenes) > 4:
            raise ValueError("No se pueden asociar más de 4 imágenes a una noticia.")

        # 2. Crear la noticia principal
        noticia = self.create(
            FonoApp_Administracion=usuario,
            titulo=titulo,
            contenido=contenido,
            **extra_fields
        )

        # 3. Si vienen imágenes, guardarlas en la tabla relacionada
        if imagenes:
            # Importación local para evitar un error de "importación circular" con models.py
            from .models import FonoApp_Noticia_Imagen 
            
            # Usamos bulk_create para guardar todas las imágenes en 1 sola consulta SQL
            imagenes_objs = [
                FonoApp_Noticia_Imagen(noticia=noticia, imagen=img) 
                for img in imagenes
            ]
            FonoApp_Noticia_Imagen.objects.bulk_create(imagenes_objs)

        return noticia