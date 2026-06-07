from rest_framework import serializers
from FonoAppAdministracion.models import FonoApp_Administracion

class FonoApp_Serializer(serializers.ModelSerializer):
    # Añadimos el estilo de password para la interfaz web
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = FonoApp_Administracion
        fields = ['id_usuario', 'nombre', 'rut', 'email', 'tipo', 'estado', 'is_staff', 'password', 'last_conection']
        read_only_fields = ['id_usuario']

    def create(self, validated_data):
        # Llamamos al método personalizado del QuerySet
        return FonoApp_Administracion.objects.crear_usuario(**validated_data)

    def update(self, instance, validated_data):
        # Extraemos el password del diccionario de datos (si no viene, devuelve None)
        password = validated_data.pop('password', None)
        
        # Dejamos que DRF actualice el resto de los campos (nombre, rut, etc.)
        # Esto maneja automáticamente la lógica de PUT vs PATCH
        instance = super().update(instance, validated_data)
        
        # Si en la petición enviaron un password, lo encriptamos
        if password:
            instance.set_password(password) # set_password encripta automáticamente
            instance.save() # Guardamos el cambio de la contraseña
            
        return instance