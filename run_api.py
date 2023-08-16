import uvicorn

from api.app import create_app
from api.settings import settings

app = create_app(settings.is_local)

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
