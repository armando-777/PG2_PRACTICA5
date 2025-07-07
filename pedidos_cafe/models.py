from django.db import models
from django.core.exceptions import ValidationError
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder
# Create your models here.

class PedidoCafe(models.Model):
    cliente = models.CharField(max_length=100)
    tipo_base = models.CharField(
        max_length=20,
        choices=[
            ("espresso", "Espresso"),
            ("americano", "Americano"),
            ("latte", "Latte"),
        ],
    )
    ingredientes = models.JSONField(default=list)
    tamanio = models.CharField(
        max_length=10,
        choices=[
            ("pequeño", "Pequeño"),
            ("mediano", "Mediano"),
            ("grande", "Grande"),
        ],
    )
    fecha = models.DateTimeField(auto_now_add=True)


    def clean(self):
        # Esta función se ejecuta automáticamente cuando se guarda el modelo desde el admin

        cafe = CafeFactory.obtener_base("espresso")
        builder = CafePersonalizadoBuilder(cafe)

        ingredientes_invalidos = []

        for ingrediente in self.ingredientes:
            try:
                builder.agregar_ingrediente(ingrediente)
            except ValueError:
                ingredientes_invalidos.append(ingrediente)

        if ingredientes_invalidos:
            raise ValidationError({
                'ingredientes': (
                    f"Ingredientes no válidos: {ingredientes_invalidos}. "
                    f"Los permitidos son: ['canela', 'chocolate', 'vainilla', 'azucar', 'leche extra']"
                )
            })