from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.game.dao import UserDAO
from app.game.schemas import SetBestScoreResponse, SetBestScoreRequest, TelegramIDModel

router = APIRouter(prefix="", tags=["Game"])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('pages/index.html', {"request": request})


@router.put("/api/bestScore/{user_id}", response_model=SetBestScoreResponse, summary="Set Best Score")
async def set_best_score(user_id: int, request: SetBestScoreRequest, session: AsyncSession = Depends(get_session)):
    score = request.score
    user = await UserDAO.find_one_or_none(session, filters=TelegramIDModel(telegram_id=user_id))
    user.best_score = score
    await session.commit()
    return SetBestScoreResponse(status="Success", best_score=score)


@router.get("/records", response_class=HTMLResponse)
async def read_records(request: Request, session: AsyncSession = Depends(get_session)):
    records = await UserDAO.get_top_scores(session)
    return templates.TemplateResponse("pages/records.html", {"request": request, "records": records})
