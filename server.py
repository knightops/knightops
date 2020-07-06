import uvicorn
from core import init_application

app_name = 'app'
app = init_application(app_name)

if __name__ == "__main__":
    uvicorn.run(app="server:app", host='0.0.0.0', port=8089, log_level='info', reload=True, workers=2)
