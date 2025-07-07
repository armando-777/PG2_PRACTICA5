from rest_framework import serializers
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder, CafeDirector
from api_patrones.logger import Logger


class PedidoCafeSerializer(serializers.ModelSerializer):
    precio_total = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()

    class Meta:
        model = PedidoCafe
        fields = [
            "id",
            "cliente",
            "tipo_base",
            "ingredientes",
            "tamanio",
            "fecha",
            "precio_total",
            "ingredientes_finales",
        ]

    def get_precio_total(self, obj):
        # Patron Factory
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        # Patron Builder
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        # Patron Singleton
        Logger().registrar(f"Se registró el calculo del precio para el pedido {obj.id}")
        print(Logger().obtener_logs())
        return builder.obtener_precio()

    def get_ingredientes_finales(self, obj):
        # Patron Factory
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        # Patron Builder
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        # Patron Singleton
        Logger().registrar(
            f"Se registró la obtención de ingredientes finales para el pedido {obj.id}"
        )
        print(Logger().obtener_logs())
        return builder.obtener_ingredientes_finales()
    

    def validate_ingredientes(self, value):
        # Crear un builder temporal con cualquier base
        cafe_dummy = CafeFactory.obtener_base("espresso")
        builder = CafePersonalizadoBuilder(cafe_dummy)

        # Obtenemos la lista de ingredientes válidos desde el builder
        precios_validos = {
            "canela": 1,
            "chocolate": 2,
            "vainilla": 1.5,
            "azucar": 0.5,
            "leche extra": 2,
        }

        ingredientes_invalidos = [
            ingrediente for ingrediente in value if ingrediente not in precios_validos
        ]

        if ingredientes_invalidos:
            raise serializers.ValidationError(
                f"Ingredientes no válidos: {ingredientes_invalidos}. "
                f"Los permitidos son: {list(precios_validos.keys())}"
            )

        return value