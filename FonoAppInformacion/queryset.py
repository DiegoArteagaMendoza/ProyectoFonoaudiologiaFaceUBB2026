from django.db import models

class FonoApp_Informacion_Queryset(models.QuerySet):

    # =========================================================
    # MÉTODOS DE BÚSQUEDA Y FILTRO
    # =========================================================

    def activas(self):
        """
        Retorna solo los registros que no han sido eliminados lógicamente.
        """
        return self.filter(estado=True)

    def con_detalles(self):
        """
        ¡Crucial para el rendimiento! Trae al autor (select_related) y 
        a las imágenes (prefetch_related) en la misma consulta para evitar el N+1.
        """
        return self.select_related('FonoApp_Administracion').prefetch_related('imagenes')

    def por_categoria(self, categoria_codigo):
        """
        Filtra por el código de la categoría (Ej: 'SA' para Salud Animal).
        """
        return self.filter(categoria=categoria_codigo)


    # =========================================================
    # MÉTODOS DE CREACIÓN, EDICIÓN Y ELIMINACIÓN
    # =========================================================

    def crear_informacion(self, usuario, titulo, categoria, contenido, imagenes=None, **extra_fields):
        """
        Crea el registro y asocia hasta 4 imágenes en bloque.
        """
        # 1. Validar límite de imágenes
        if imagenes and len(imagenes) > 4:
            raise ValueError("No se pueden asociar más de 4 imágenes.")

        # 2. Crear registro principal
        informacion = self.create(
            FonoApp_Administracion=usuario,
            titulo=titulo,
            categoria=categoria,
            contenido=contenido,
            **extra_fields
        )

        # 3. Guardar imágenes si existen usando bulk_create
        if imagenes:
            # Importación local para evitar importación circular
            from .models import FonoApp_Informacion_Imagen 
            
            imagenes_objs = [
                FonoApp_Informacion_Imagen(informacion=informacion, imagen=img) 
                for img in imagenes
            ]
            FonoApp_Informacion_Imagen.objects.bulk_create(imagenes_objs)

        return informacion

    def editar_informacion(self, id_informacion, **datos_a_actualizar):
        """
        Actualiza los campos de texto del registro de forma masiva y eficiente.
        Ejemplo de uso: .editar_informacion(1, titulo="Nuevo", categoria="CU")
        """
        # Limpiamos datos que no deberían actualizarse por esta vía (por seguridad)
        datos_a_actualizar.pop('FonoApp_Administracion', None)
        datos_a_actualizar.pop('imagenes_subidas', None) # Las imágenes se manejan aparte
        
        # El update() retorna el número de filas afectadas (1 si fue exitoso, 0 si falló)
        filas_actualizadas = self.filter(id_informacion=id_informacion, estado=True).update(**datos_a_actualizar)
        
        return filas_actualizadas > 0

    def eliminar_logico(self, id_informacion):
        """
        Oculta el registro cambiando estado=False en lugar de borrarlo de la BD.
        """
        filas_actualizadas = self.filter(id_informacion=id_informacion).update(estado=False)
        return filas_actualizadas > 0