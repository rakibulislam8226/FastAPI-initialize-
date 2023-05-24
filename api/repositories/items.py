from api.models import Items
from api.utils import generate_ping_id
from api.repositories.base import BaseRepository
from sqlalchemy import select, cast, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import ItemsSchema


class ItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Items
        self.item_id = None
        self.title = None
        self.description = None
        self.is_active = False
        self.items_number = None
        self.data = None
        # self.vertical_fields = []
        self.ping_log = None

    
    async def process_data(self, session: AsyncSession, data: dict) -> dict:
        self.session = session
        self.item_id = generate_ping_id()
        self.data = data['data']

        ping_log_payload_data = ItemsSchema(
            item_id=self.item_id,
            ip_address=data['data']['ip_address'],
            is_active=False,
            title=data['data']['title'],
            description=data['data']['description'],
            items_number=data['data']['items_number'],
        ).dict()

    
        # Check if items_number exists
        if not self.data.get('title'):
            response_data = {
                "result": "failed",
                "price": 0.00,
                "message": "Invalid Request",
                "errors": [
                    {
                        "error": "Missing Items title or description."
                    }
                ]
            }
            ping_log_payload_data.update({
                'response': response_data
            })
            ping_log_payload = ItemsSchema(**ping_log_payload_data)
            # self.ping_log = await self.create(self.session, **ping_log_payload.dict())
            return response_data
        

        # If everything's allright, save and respond to seller
        # TODO: Calculate and update data on previous steps completion
        ping_log_payload_data.update({
            'item_accepted': True,
        })
        ItemsSchema(**ping_log_payload_data) # Validate

        response_data = {
            "result": "Success",
            "item_id": self.item_id,
            "price": 0.00,
            "message": "Item accept",
        }
        
        ping_log_payload_data.update({
            'response': response_data,
        })
        ping_log_payload = ItemsSchema(**ping_log_payload_data) # Validate
        self.ping_log = await self.create(self.session, **ping_log_payload.dict())
        return response_data

        