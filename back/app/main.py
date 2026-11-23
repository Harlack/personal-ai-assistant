from fastapi import FastAPI
from app.notes.router import router
from app.notes.exceptions import NoteNotFoundException
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(router)


@app.exception_handler(NoteNotFoundException)
async def note_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/info")
async def read_info():
    return {
                "name": "Personal AI Assistant",
                "version": "0.1.0"
    }

@app.get("/health")
async def read_health():
    return {"status": "healthy"}

