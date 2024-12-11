from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
tmpl = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int = None
    username: str = None
    age: int = None


@app.get('/')
async def get_main_page(request: Request):
    return tmpl.TemplateResponse("users.html", {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: int):
    try:
        user = next(user for user in users if user.id == user_id)
        return tmpl.TemplateResponse("users.html", {'request': request, 'user': user})
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/user/{username}/{age}')
async def add_user(user: User,
                   username: str = Path(min_length=5, max_length=20, description='Enter username', example='NewUser'),
                   age: int = Path(ge=18, le=120, description='Enter User age', example='19')) -> str:
    user.id = 1 if len(users) == 0 else len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f'User {user.id} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int,
                      username: str = Path(min_length=5, max_length=20, description='Enter username',
                                           example='NewUser'),
                      age: int = Path(ge=18, le=120, description='Enter User age', example='19')) -> str:
    try:
        edit_user = next(user for user in users if user.id == user_id)
        edit_user.username = username
        edit_user.age = age
        return f'User {user_id} has been updated.'
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        del_user = next(user for user in users if user.id == user_id)
        users.remove(del_user)
        return f'User {user_id} has been deleted.'
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')
