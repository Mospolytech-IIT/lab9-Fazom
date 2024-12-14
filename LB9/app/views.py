from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_302_FOUND
from app.database import get_db
from app.crud import create_user, get_users, create_post, get_posts
from app.models import User, Post

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Маршрут для отображения списка пользователей
@router.get("/users", response_class=HTMLResponse)
async def users_list(request: Request, db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

# Маршрут для создания пользователя
@router.get("/users/new", response_class=HTMLResponse)
async def new_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})

@router.post("/users/new", response_class=HTMLResponse)
async def create_user_route(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await create_user(db, username=username, email=email, password=password)
    return RedirectResponse(url="/users", status_code=HTTP_302_FOUND)

# Маршрут для отображения списка постов
@router.get("/posts", response_class=HTMLResponse)
async def posts_list(request: Request, db: AsyncSession = Depends(get_db)):
    posts = await get_posts(db)
    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": posts})

# Маршрут для создания поста
@router.get("/posts/new", response_class=HTMLResponse)
async def new_post_form(request: Request):
    return templates.TemplateResponse("post_form.html", {"request": request})

@router.post("/posts/new", response_class=HTMLResponse)
async def create_post_route(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await create_post(db, title=title, content=content, user_id=user_id)
    return RedirectResponse(url="/posts", status_code=HTTP_302_FOUND)

# Дополнительно: маршруты для редактирования и удаления записей
@router.get("/users/delete/{user_id}", response_class=HTMLResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return RedirectResponse(url="/users", status_code=HTTP_302_FOUND)

@router.get("/posts/delete/{post_id}", response_class=HTMLResponse)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_302_FOUND)

# Редактирование пользователя
@router.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user(request: Request, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user_form.html", {"request": request, "user": user})

@router.post("/users/edit/{user_id}", response_class=HTMLResponse)
async def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(None),  # Пароль не обязателен для редактирования
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = username
    user.email = email
    if password:  # Если пароль был введен, обновляем его
        user.password = password
    
    await db.commit()
    return RedirectResponse(url="/users", status_code=303)

# Редактирование поста
@router.get("/posts/edit/{post_id}", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post_form.html", {"request": request, "post": post})

@router.post("/posts/edit/{post_id}", response_class=HTMLResponse)
async def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    post = await db.get(Post, post_id)  # Получаем пост по ID
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")  # Если не найден, ошибка 404
    
    post.title = title  # Обновляем заголовок
    post.content = content  # Обновляем содержимое
    
    await db.commit()  # Сохраняем изменения в базе данных
    return RedirectResponse(url="/posts", status_code=303)  # Перенаправляем на список постов

