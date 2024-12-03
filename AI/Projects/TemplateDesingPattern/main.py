from fastapi import FastAPI
import uvicorn
from app_router.route import router
app = FastAPI(title="Chat Server", version="1.0", description="Api integration with chatbot")
app.include_router(router)
#
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
