from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/chart", response_class=HTMLResponse)
def chart_page(request: Request):
    return templates.TemplateResponse(
        "chart.html",
        {
            "request": request
        }
    )