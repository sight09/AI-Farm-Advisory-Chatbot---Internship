# import asyncio
# from services.ingestion.embed_and_store import embed_and_store
# from common.core.openai_client import single_embed
# from common.models.user import User
# from common.models.document import Document
# from common.models.db import SessionLocal
# from common.models import init_db
# from common.core.openweather import get_weather


# async def test_embed_and_store():
#     init_db()
#     db = SessionLocal()
    
#     try:
#         weather = await get_weather("London", units="metric", lang="en")
#         print(weather)
        
#     except Exception as e:
#         print(f"Error during test setup: {e}")
#     finally:
#         db.close()
    
# asyncio.run(test_embed_and_store())


# # asyncio.run(embed_and_store("services/ingestion/raw/hess403.pdf", title="Hess 403 Syllabus"))



# print("Starting embedding and storage process...")


import click
import sys
import asyncio
from common.models.db import SessionLocal
from common.models import init_db


# If no arguments are provided, exit gracefully
if len(sys.argv) == 1:
    print("No command provided. Exiting.")
    sys.exit(0)


@click.group(help="⚙️  CLI Tool to manage backend tasks and services.")
def cli():
    pass


@cli.command(help="Run the backend server.")
def runserver():
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)

@cli.command(help="Run embed and store")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--title", default=None, help="Optional title for the document.")
def embed_and_store_cmd(file_path, title):
    from services.ingestion.embed_and_store import embed_and_store

    async def run_embed_and_store():
        init_db()
        try:
            await embed_and_store(file_path, title=title)
        except Exception as e:
            print("[Error] Embedding error")

    asyncio.run(run_embed_and_store())


@cli.command(help="Run the Telegram bot.")
def runbot():
    from services.bot.handlers.bot import init_bot
    init_bot()

    


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt as e:
        print("\n\033[91mProcess interrupted by user.\033[0m")
        sys.exit(0)