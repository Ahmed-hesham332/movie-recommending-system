from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .recommender import recommend_movies

app = FastAPI()
templates = Jinja2Templates(directory="./src/templates")
app.mount("/static", StaticFiles(directory="./src/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/recommend")
async def get_recommendations(movie_name: str):
    recommendations = recommend_movies(movie_name)

    if isinstance(recommendations, str):
        return {"error": recommendations}

    return recommendations.to_dict(orient="records") 
