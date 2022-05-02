from api import create_app
import uvicorn
from os import environ

app = create_app()

PORT = environ.get('PORT', 5000)
DEBUG = environ.get('DEBUG', False)

if __name__ == "__main__":
    uvicorn.run("__main__:app",host = '0.0.0.0',port = PORT, reload = True)