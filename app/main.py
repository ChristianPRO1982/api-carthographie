from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime
import subprocess
from pathlib import Path
from docx import Document
import fitz  # PyMuPDF
# from utils import cARThographieDB # PROD
from .utils import cARThographieDB # DEV


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.carthographie.fr",
        "https://carthographie.fr",
        "https://api.carthographie.fr"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/nb_pages", summary="1 page = X songs", tags=["API"])
async def get_pages():
    """
    # 1 page = X songs / 1 page = X chansons
    - this API return the number of pages for find all songs
    - cette API retourne le nombre de pages pour trouver toutes les chansons
    """
    db = cARThographieDB()
    pages = db.get_all_songs_pages()
    return pages


@app.get("/table_c_artists", summary="Artists", tags=["cARThographie"])
async def table_c_artists(api_key: str = Query(..., description="API Key for access")):
# async def table_artists(page: int = Query(1, gt=0)):
    """
    # all artists
    ## json
    - DUMP of c_artists table
    - only INSERT SQL command
    
    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_artists?api_key=abcde
    """
    db = cARThographieDB()
    artists = db.table_c_artists(api_key)
    if "error" in artists:
        return JSONResponse(status_code=401, content=artists)
    return JSONResponse(content=artists)


@app.get("/table_c_artist_links", summary="Artist Links", tags=["cARThographie"])
async def table_c_artist_links(api_key: str = Query(..., description="API Key for access")):
    """
    # all artist links
    ## json
    - DUMP of c_artist_links table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_artist_links?api_key=abcde
    """
    db = cARThographieDB()
    artist_links = db.table_c_artist_links(api_key)
    if "error" in artist_links:
        return JSONResponse(status_code=401, content=artist_links)
    return JSONResponse(content=artist_links)


@app.get("/table_c_bands", summary="Bands", tags=["cARThographie"])
async def table_c_bands(api_key: str = Query(..., description="API Key for access")):
    """
    # all bands
    ## json
    - DUMP of c_bands table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_bands?api_key=abcde
    """
    db = cARThographieDB()
    bands = db.table_c_bands(api_key)
    if "error" in bands:
        return JSONResponse(status_code=401, content=bands)
    return JSONResponse(content=bands)


@app.get("/table_c_bands_links", summary="Bands Links", tags=["cARThographie"])
async def table_c_bands_links(api_key: str = Query(..., description="API Key for access")):
    """
    # all bands links
    ## json
    - DUMP of c_band_links table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_bands_links?api_key=abcde
    """
    db = cARThographieDB()
    band_links = db.table_c_band_links(api_key)
    if "error" in band_links:
        return JSONResponse(status_code=401, content=band_links)
    return JSONResponse(content=band_links)


@app.get("/table_c_group_user", summary="Group User", tags=["cARThographie"])
async def table_c_group_user(api_key: str = Query(..., description="API Key for access")):
    """
    # all group users
    ## json
    - DUMP of c_group_user table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_group_user?api_key=abcde
    """
    db = cARThographieDB()
    group_users = db.table_c_group_user(api_key)
    if "error" in group_users:
        return JSONResponse(status_code=401, content=group_users)
    return JSONResponse(content=group_users)


@app.get("/table_c_group_user_ask_to_join", summary="Group User Ask to Join", tags=["cARThographie"])
async def table_c_group_user_ask_to_join(api_key: str = Query(..., description="API Key for access")):
    """
    # all group user ask to join
    ## json
    - DUMP of c_group_user_ask_to_join table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_group_user_ask_to_join?api_key=abcde
    """
    db = cARThographieDB()
    group_user_ask_to_join = db._table_group_user_ask_to_join(api_key)
    if "error" in group_user_ask_to_join:
        return JSONResponse(status_code=401, content=group_user_ask_to_join)
    return JSONResponse(content=group_user_ask_to_join)


@app.get("/table_c_groups", summary="Groups", tags=["cARThographie"])
async def table_c_groups(api_key: str = Query(..., description="API Key for access")):
    """
    # all groups
    ## json
    - DUMP of c_groups table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_groups?api_key=abcde
    """
    db = cARThographieDB()
    groups = db.table_c_groups(api_key)
    if "error" in groups:
        return JSONResponse(status_code=401, content=groups)
    return JSONResponse(content=groups)


@app.get("/table_c_user_change_email", summary="User Change Email", tags=["cARThographie"])
async def table_c_user_change_email(api_key: str = Query(..., description="API Key for access")):
    """
    # all user change email requests
    ## json
    - DUMP of c_user_change_email table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_user_change_email?api_key=abcde
    """
    db = cARThographieDB()
    user_change_email = db.table_c_user_change_email(api_key)
    if "error" in user_change_email:
        return JSONResponse(status_code=401, content=user_change_email)
    return JSONResponse(content=user_change_email)


@app.get("/table_c_users", summary="Users", tags=["cARThographie"])
async def table_c_users(api_key: str = Query(..., description="API Key for access")):
    """
    # all users
    ## json
    - DUMP of c_users table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_users?api_key=abcde
    """
    db = cARThographieDB()
    users = db.table_c_users(api_key)
    if "error" in users:
        return JSONResponse(status_code=401, content=users)
    return JSONResponse(content=users)


@app.get("/table_l_genres", summary="Genres", tags=["lyrics"])
async def table_l_genres(api_key: str = Query(..., description="API Key for access")):
    """
    # all genres
    ## json
    - DUMP of c_genres table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_c_genres?api_key=abcde
    """
    db = cARThographieDB()
    genres = db.table_l_genres(api_key)
    if "error" in genres:
        return JSONResponse(status_code=401, content=genres)
    return JSONResponse(content=genres)


@app.get("/table_l_site", summary="Lyrics Sites", tags=["lyrics"])
async def table_l_site(api_key: str = Query(..., description="API Key for access")):
    """
    # all lyrics sites
    ## json
    - DUMP of l_site table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_l_site?api_key=abcde
    """
    db = cARThographieDB()
    lyrics_sites = db.table_l_site(api_key)
    if "error" in lyrics_sites:
        return JSONResponse(status_code=401, content=lyrics_sites)
    return JSONResponse(content=lyrics_sites)


@app.get("/table_l_site_params", summary="Lyrics Site Params", tags=["lyrics"])
async def table_l_site_params(api_key: str = Query(..., description="API Key for access")):
    """
    # all lyrics site params
    ## json
    - DUMP of l_site_params table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_l_site_params?api_key=abcde
    """
    db = cARThographieDB()
    lyrics_site_params = db.table_l_site_params(api_key)
    if "error" in lyrics_site_params:
        return JSONResponse(status_code=401, content=lyrics_site_params)
    return JSONResponse(content=lyrics_site_params)


@app.get("/table_l_songs", summary="Songs", tags=["lyrics"])
async def table_l_songs(api_key: str = Query(..., description="API Key for access")):
    """
    # all songs
    ## json
    - DUMP of l_songs table
    - only INSERT SQL command

    ## doc
    - **api_key:** secret key to access this endpoint

    ## url
    - /table_l_songs?api_key=abcde
    """
    db = cARThographieDB()
    songs = db.table_l_songs(api_key)
    if "error" in songs:
        return JSONResponse(status_code=401, content=songs)
    return JSONResponse(content=songs)


@app.get("/health", summary="API ready?", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/about", tags=["Meta"])
async def about():
    """
    # cARThographie API Features / Fonctionnalités de l'API cARThographie

    ## SONGS

    ### /nb_pages
    - Get the number of pages for all songs.
    - Obtenez le nombre de pages pour toutes les chansons.

    ### /songs_title
    - Get all songs (only title).
    - Obtenez toutes les chansons (seulement le titre).

    ### /songs_verses
    - Get all songs with choruses/verses.
    - Obtenez toutes les chansons avec refrains/couplets.

    ### /songs_full
    - Get all songs with one HTML field for all song's text.
    - Obtenez toutes les chansons avec un champ HTML pour tout le texte de la chanson.
    
    ## other features

    ### /health
    - Check if the API is running and ready to use.
    - Vérifiez si l'API fonctionne et est prête à être utilisée.
    """
    return JSONResponse(
        content={
            "message": (
                "All features here : api.carthographie.fr/docs#/Meta/about_about_get"
            )
        }
    )


GITHUB_API = "https://api.github.com/repos/ChristianPRO1982/api-carthographie/releases/latest"
@app.get("/version", summary="GitHub version", tags=["Meta"])
async def version():
    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_API)
        if response.status_code == 200:
            data = response.json()
            return {
                "tag_name": data.get("tag_name"),
                "published_at": data.get("published_at"),
                "badge": "https://img.shields.io/github/release/ChristianPRO1982/api-carthographie.svg"
            }
        else:
            return {"error": "Impossible de récupérer la version GitHub"}


@app.post("/convert_pdf_to_txt", summary="Convert PDF or DOCX to TXT", tags=["Conversion"])
def convert_pdf_to_txt():
    input_path = Path("/files/contrat.pdf")
    output_path = Path("/files/contrat.txt")

    if not input_path.exists():
        return {"success": False, "error": "File not found"}

    try:
        text = extract_text_from_pdf(input_path)

        output_path.write_text(text)
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

@app.post("/convert_docx_to_txt", summary="Convert DOCX or DOC to TXT", tags=["Conversion"])
def convert_docx_to_txt():
    input_path = Path("/files/contrat.docx")
    output_path = Path("/files/contrat.txt")

    if not input_path.exists():
        return {"success": False, "error": "File not found"}

    try:
        text = extract_text_from_docx(input_path)

        output_path.write_text(text)
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)


def extract_text_from_docx(docx_path: Path) -> str:
    doc = Document(docx_path)
    return "\n".join(p.text for p in doc.paragraphs)