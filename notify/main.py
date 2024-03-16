from datetime import date, timedelta
from time import sleep

import keyring
import requests
import typer
from decouple import config
from keyring.errors import NoKeyringError
from scrapers.scrape import scrape_amazon_ebook, scrape_scorp
from typing_extensions import Annotated

HALF_AN_HOUR = 30 * 60
HEARTBEAT = "Notify App still up and running"

app = typer.Typer(add_completion=False, rich_markup_mode="markdown")
scrapers = [scrape_scorp, scrape_amazon_ebook]

try:
    topic = keyring.get_password("ntfy", "topic")
except NoKeyringError:
    topic = config("TOPIC")

url = f"https://ntfy.sh/{topic}"


@app.command()
def publish(
    message: Annotated[str, typer.Argument()],
    priority: Annotated[int, typer.Option(min=1, max=5)] = 1,
):
    """
    **Publish** a manually entered message
    """

    requests.post(
        url,
        data=message.encode(encoding="utf-8"),
        headers={
            "Priority": str(priority),
            "Tags": "snake",
        },
    )


@app.command()
def run():
    last_heartbeat = date.today() - timedelta(days=1)
    while True:
        for scraper in scrapers:
            if message := scraper():
                publish(message)

        if (today := date.today()) > last_heartbeat:
            publish(HEARTBEAT)
            last_heartbeat = today

        sleep(HALF_AN_HOUR)


if __name__ == "__main__":
    app()
