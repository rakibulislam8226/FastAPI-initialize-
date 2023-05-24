from api.models import Items
from api.utils import generate_ping_id
from api.repositories.base import BaseRepository
from sqlalchemy import select, cast, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import ItemsSchema


class ItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.item_id = None
        self.model = Items
        self.title = None
        self.description = None
        self.is_active = False
        self.items_number = None
        self.data = None
        # self.vertical_fields = []

    
    async def process_data(self, session: AsyncSession, data: dict) -> dict:
        self.session = session
        self.item_id = generate_ping_id()
        self.data = data['data']

        print(f'============ {self.item_id}')   

        item_payload_data = ItemsSchema(
            item_id=self.item_id,
            ip_address=data['data']['ip_address'],
            is_active=False,
            title=0,
            description=None,
            items_number=0,
        ).dict()

    
        # Check if items_number exists
        if not self.data.get('items_number'):
            response_data = {
                "result": "failed",
                "price": 0.00,
                "message": "Invalid Request",
                "errors": [
                    {
                        "error": "Missing items number or Key"
                    }
                ]
            }
            item_payload_data.update({
                'response': response_data
            })
            ping_log_payload = ItemsSchema(**item_payload_data)
            self.ping_log = await self.create(self.session, **ping_log_payload.dict())
            return response_data
        

        # If everything's allright, save and respond
        item_payload_data.update({
            'ping_accepted': True,
        })
        ItemsSchema(**item_payload_data) # Validate

        response_data = {
            "result": "Success",
            "item_id": self.item_id,
            "price": 0.00,
            "message": "Item accept",
        }
        
        item_payload_data.update({
            'response': response_data,
        })
        ping_log_payload = ItemsSchema(**item_payload_data) # Validate
        # self.item_id = await self.create(self.session, **ping_log_payload.dict())
        print('inside')
        return response_data

        