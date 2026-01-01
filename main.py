from http.client import responses

from fastapi import FastAPI, Request, Form, Depends, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import Base, engine, SessionLocal
from models import User,Post
from routers.chart import router as chart_router
app = FastAPI()
app.include_router(chart_router)
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 테이블 생성
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@app.post("/signup", response_class=HTMLResponse)
def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip()

    # 간단 검증
    if len(username) < 3:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "아이디는 3자 이상"})
    password = password.strip()

    if len(password) < 8:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "비밀번호는 8자 이상"}
        )

    password_bytes = password.encode("utf-8")[:72]
    pw = password  # 네가 받은 password 변수
    print("PW repr:", repr(pw))
    print("PW type:", type(pw))
    print("PW len(chars):", len(pw))
    print("PW len(bytes):", len(pw.encode("utf-8")))
    hashed = pwd_context.hash(password_bytes)

    # 중복 체크
    exists = db.query(User).filter(User.username == username).first()
    if exists:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "이미 존재하는 아이디"})

    # 비밀번호 해시 저장
    hashed = pwd_context.hash(password)
    user = User(username=username, password_hash=hashed)
    db.add(user)
    db.commit()

    # 가입 성공 -> 로그인 페이지로 이동(예시)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/posts/new",response_class = HTMLResponse)
def post_new(request: Request):
    return templates.TemplateResponse("posts.html", {"request": request})

@app.post("/posts", response_class=HTMLResponse)
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    post = Post(
        title=title,
        content=content
    )

    db.add(post)      # ✅ 객체 추가
    db.commit()       # ✅ 실제 DB 반영
    db.refresh(post)  # ✅ id 같은 값 다시 읽기

    return HTMLResponse("글 작성 완료")


