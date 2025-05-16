from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import httpx
from fastapi.responses import RedirectResponse
from .utils import cARThographieDB

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# @app.get("/songs_title", summary="all songs (only title)", tags=["Songs"])
async def get_songs():
    """
    # all songs / toutes les chansons
    - Retrieve all songs from the database:
      - full title
      - web link (URL)
    - Obtenez toutes les chansons de la base de données :
      - titre complet
      - lien web (URL)
    """
    db = cARThographieDB()
    songs = db.get_all_songs_title()
    return songs

# @app.get("/songs_verses", summary="all songs (choruses/verses)", tags=["Songs"])
async def get_songs_verses():
    """
    # all songs with choruses/verses / toutes les chansons avec refrains/couplets
    - Retrieve all songs from the database:
      - full title
      - web link (URL)
      - choruses/verses
    - Obtenez toutes les chansons de la base de données :
      - titre complet
      - lien web (URL)
      - refrains/couplets
    
    ## doc
    - **full_title:** full title of the song / titre complet de la chanson
    - **url:** web link to the song / lien web vers la chanson
    - **text:** text of chorus/verse / texte du refrain/couplet
    - **num:** technical number of chorus/verse (real position) / numéro technique du refrain/couplet (position réelle)
    - **num_verse:** number of chorus/verse (display number) / numéro du refrain/couplet (numéro d'affichage)
    - **chorus:** 0 = verse, 1 = chorus, 2 = verse like a chorus (same order like a verse but diplayed like a chorus) / 0 = couplet, 1 = refrain, 2 = couplet comme un refrain (même ordre qu'un couplet mais affiché comme un refrain)
    - **followed:** 0 = not followed, 1 = followed (followed by the next verse) / 0 = non suivi, 1 = suivi (suivi par le couplet suivant)
    """
    db = cARThographieDB()
    songs_verses = db.get_all_songs_verses()
    return songs_verses

@app.get("/songs_full", summary="all songs (full text)", tags=["Songs"])
async def get_all_songs_full():
    """
    # all songs with full text / toutes les chansons avec texte complet
    - Retrieve all songs from the database:
      - full title
      - web link (URL)
      - full text: only one field for all song's text
    - Obtenez toutes les chansons de la base de données :
      - titre complet
      - lien web (URL)
      - texte complet : un seul champ pour tout le texte de la chanson
    """
    db = cARThographieDB()
    songs_verses = db.get_all_songs_full()
    return songs_verses

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

    ### /songs_title
    - Get all songs (only title).
    - Obtenez toutes les chansons (seulement le titre).
    
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
