import json
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "Conexão WebSocket estabelecida!"}))

    async def disconnect(self, close_code):
        print(f"Desconectado: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Mensagem recebida: {data}")
        await self.send(json.dumps({"response": "Mensagem recebida com sucesso!"}))
class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_code = self.scope['url_route']['kwargs']['match_code']
        self.group_name = f"match_{self.match_code}"

        # Adiciona o WebSocket ao grupo
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o WebSocket do grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Recebe mensagem do WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Envia mensagem para o grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    # Recebe mensagem do grupo
    async def chat_message(self, event):
        message = event['message']

        # Envia mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
