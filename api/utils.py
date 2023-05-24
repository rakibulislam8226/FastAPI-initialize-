import uuid
from json import JSONDecodeError
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request


def generate_ping_id(string_length: int = 10) -> str:
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()).upper().replace("-", "")  # Convert UUID format to a Python string.
    return random[0:string_length]  # Return the random string.


async def check_content_type_and_get_data(request: Request) -> dict:
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        url_params = request.query_params
        if url_params:
            data = url_params._dict
            return {
                'method': 'GET',
                'content_type': '',
                'data': data
            }
        raise HTTPException(status_code=400, detail='No Content-Type provided!')
    
    elif content_type == 'application/json':
        try:
            data = await request.json()
        except JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    elif (content_type == 'application/x-www-form-urlencoded' or
          content_type.startswith('multipart/form-data')):
        try:
            data = await request.form()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    else:
        raise HTTPException(status_code=400, detail='Content-Type not supported!')
    
    return {
        'method': 'POST',
        'content_type': content_type,
        'data': jsonable_encoder(data)
    }