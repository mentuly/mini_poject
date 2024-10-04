from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl, BaseModel, Field
import httpx
from bs4 import BeautifulSoup
from .. import app

async def fetch_page(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            responce = await client.get(url)
            responce.raise_for_status()
            return responce.text
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=responce.status_code, detail="Error fetching the page")
    except Exception as e:
        raise HTTPException(status_code=400, datail="Invalid URL or can't fetch the page")
    
def parse_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    headers = {
        "h1": [h.get_text() for h in soup.find_all('h1')],
        "h2": [h.get_text() for h in soup.find_all('h2')],
        "h3": [h.get_text() for h in soup.find_all('h3')],
        "h4": [h.get_text() for h in soup.find_all('h4')],
        "h5": [h.get_text() for h in soup.find_all('h5')]
    }

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/paser/")
async def parse_url(url: HttpUrl):
    html_content = await fetch_page(str(url))
    parse_data = parse_html(html_content)
    return parse_data