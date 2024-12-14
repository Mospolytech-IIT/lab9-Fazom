from fastapi import FastAPI
from app.views import router

app = FastAPI()

# Подключение маршрутов
app.include_router(router)

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
