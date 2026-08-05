from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
# Usamos el mismo arreglo para GET/POST y para PUT/PATCH/DELETE.
data_list = []

# Esta forma es más dinámica porque permite cargar datos desde una lista de ejemplo
# y agregar cada elemento con append. Es útil cuando luego quieras reutilizar este
# patrón para muchos datos o para leerlos desde un archivo o una API.
sample_data = [
    {'name': 'Elemento Uno', 'email': 'user01@example.com', 'is_active': True},
    {'name': 'Elemento Dos', 'email': 'user02@example.com', 'is_active': True},
    {'name': 'Elemento Tres', 'email': 'user03@example.com', 'is_active': False},
]

for item in sample_data:
    data_list.append({
        'id': str(uuid.uuid4()),
        'name': item['name'],
        'email': item['email'],
        'is_active': item['is_active'],
    })

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):

    # --- MÉTODO PUT (Reemplazo Completo) ---
    def put(self, request, id):
        data = request.data
        
        # Validar que el identificador esté en el cuerpo de la solicitud
        if 'id' not in data:
            return Response(
                {"error": "El identificador ('id') es obligatorio en el cuerpo de la solicitud."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Validar que el ID del cuerpo coincida con el ID de la ruta URL
        if str(data['id']) != str(id):
            return Response(
                {"error": "El identificador del cuerpo no coincide con el de la URL."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el elemento activo en la lista compartida
        for item in data_list:
            if item['id'] == id and item.get('is_active', False):
                item.clear()

                item['id'] = id
                item['is_active'] = True

                for key, value in data.items():
                    if key != 'is_active':
                        item[key] = value

                return Response(
                    {"mensaje": "Elemento reemplazado completamente con éxito.", "elemento": item}, 
                    status=status.HTTP_200_OK
                )
                
        # Si no se encuentra el ID o está marcado como eliminado
        return Response(
            {"error": f"No se encontró el elemento con identificador {id} o fue eliminado."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # --- MÉTODO PATCH (Actualización Parcial) ---
    def patch(self, request, id):
        data = request.data

        # Buscar el elemento activo en la lista compartida
        for item in data_list:
            if item['id'] == id and item.get('is_active', False):
                # Actualizar solo los campos recibidos, manteniendo los no modificados
                for key, value in data.items():
                    if key != 'id' and key != 'is_active':
                        item[key] = value
                        
                return Response(
                    {"mensaje": "Elemento actualizado parcialmente con éxito.", "elemento": item}, 
                    status=status.HTTP_200_OK
                )
                
        return Response(
            {"error": f"No se encontró el elemento con identificador {id} para actualizar."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # --- MÉTODO DELETE (Eliminación Lógica) ---
    def delete(self, request, id):
        # Buscar el elemento activo en la lista compartida
        for item in data_list:
            if item['id'] == id and item.get('is_active', False):
                item['is_active'] = False
                return Response(
                    {"mensaje": f"Elemento con identificador {id} eliminado lógicamente de forma exitosa."}, 
                    status=status.HTTP_200_OK
                )
                
        return Response(
            {"error": f"El elemento con identificador {id} no existe o ya ha sido eliminado previamente."}, 
            status=status.HTTP_404_NOT_FOUND
        )