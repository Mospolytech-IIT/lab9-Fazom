from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Post

# Добавление пользователя
async def create_user(db: AsyncSession, username: str, email: str, password: str):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Получение всех пользователей
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Получение всех постов
async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post).join(User))
    return result.scalars().all()

# Добавление поста
async def create_post(db: AsyncSession, title: str, content: str, user_id: int):
    new_post = Post(title=title, content=content, user_id=user_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post
