import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.main:app", log_level="info",port=8002 ,reload=True)