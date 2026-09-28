from contextlib import asynccontextmanager
from datetime import datetime, UTC

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api import ai_services, auth, inspections, stats, vehicles, workflows
from app.core.config import settings
from app.db.database import initialize_database
from app.db.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    seed_data()
    yield


app = FastAPI(
    title="Hệ thống Quản lý Đăng kiểm Tích hợp AI",
    version=settings.APP_VERSION,
    description="API quản lý đăng kiểm phương tiện với AI hỗ trợ tư vấn quy trình, tóm tắt hồ sơ và nhắc lịch.",
    lifespan=lifespan,
)
templates = Jinja2Templates(directory="app/templates")

# Dang ky Routers
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(inspections.router)
app.include_router(stats.router)
app.include_router(ai_services.router)
app.include_router(workflows.router)

# Exception Handler: Validate Đầu vào
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Dữ liệu gửi lên không đúng định dạng.", "errors": exc.errors()},
    )

# Exception Handler: Lỗi CSDL
@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Lỗi thao tác Cơ sở dữ liệu. Vui lòng thử lại sau."},
    )

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
@app.get("/register", response_class=HTMLResponse)
async def render_auth(request: Request):
    return templates.TemplateResponse(request=request, name="auth.html")


@app.get("/app", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "dangkiem-ai-system",
        "environment": settings.ENV,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/api/health")
async def api_health_check():
    return {
        "status": "ok",
        "service": "dangkiem-ai-system",
        "environment": settings.ENV,
        "timestamp": datetime.now(UTC).isoformat(),
    }