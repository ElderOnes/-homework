from fastapi import FastAPI, Path

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: str = Path(min_length=5, max_length=20, description='Enter username',
                                        example='UrbanUser'),
                   age: int = Path(ge=18, le=120, description='Enter User ID', example='13')) -> str:
    new_user_id = str(int(max(users, key=int)) + 1)
    users[new_user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {new_user_id} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: str,
                      username: str = Path(min_length=5, max_length=20, description='Enter username',
                                           example='NewUser'),
                      age: int = Path(ge=18, le=120, description='Enter User ID', example='13')) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} has been updated.'


@app.delete('/user/{user_id}')
async def delete_user(user_id: str) -> str:
    users.pop(user_id)
    return f'User {user_id} has been deleted.'
