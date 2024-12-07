from django.urls import path
from . import consumers  # Importar consumidores do mesmo aplicativo

websocket_urlpatterns = [
    path('ws/quiz/', consumers.QuizConsumer.as_asgi()),  # Rota WebSocket
]