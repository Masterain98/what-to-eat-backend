from fastapi import FastAPI
from db.database import Base, engine
from routers import restaurant, tags
import uvicorn
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

# Initialize database
#Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the restaurant router
app.include_router(restaurant.router)
app.include_router(tags.router)


@app.get("/swagger", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8900, proxy_headers=True, forwarded_allow_ips="*")
