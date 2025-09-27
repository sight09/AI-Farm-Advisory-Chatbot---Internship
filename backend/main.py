import click
import sys
import asyncio
from common.models.db import SessionLocal
from common.models import init_db
from common.logger_utils import logger


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
    logger.info("Starting the backend server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Backend server stopped.")

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
    logger.info("Starting the Telegram bot...")
    init_bot()

    


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt as e:
        print("\n\033[91mProcess interrupted by user.\033[0m")
        sys.exit(0)