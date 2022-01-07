from api import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run("__main__:app", port=3000, reload = True)