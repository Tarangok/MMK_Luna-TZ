from fastapi import FastAPI
import uvicorn

from routes.activity import router as activity_router
from routes.building import router as building_router
from routes.organization import router as organization_router

app = FastAPI(
    title="MMK_Luna API",
    description="REST API для MMK_Luna",
    version="0.1.0",
    docs_url="/swagger"
)

app.include_router(activity_router)
app.include_router(building_router)
app.include_router(organization_router)


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080, 
        log_level="debug"
    )