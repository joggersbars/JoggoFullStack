import uvicorn
#Running server
if __name__ == '__main__':
    uvicorn.run("app.main:app",host="152.42.129.144" ,log_level="info",port=8002 ,reload=False)