from datetime import date, timedelta
from time import sleep

import keyring
import requests
import typer
from decouple import config
from keyring.errors import NoKeyringError
from scrapers.scrape import scrape_amazon_ebook, scrape_scorp
from typing_extensions import Annotated

DEFAULT_TAG = "snake"
HALF_AN_HOUR = 30 * 60
HEARTBEAT = "white_check_mark"

app = typer.Typer(add_completion=False, rich_markup_mode="markdown")
scrapers = [(scrape_scorp, "hocho"), (scrape_amazon_ebook, "book")]

try:
    topic = keyring.get_password("ntfy", "topic")
except NoKeyringError:
    topic = config("TOPIC")

url = f"https://ntfy.sh/{topic}"


@app.command()
def publish(
    message: Annotated[str, typer.Argument()],
    priority: Annotated[int, typer.Option(min=1, max=5)] = 5,
    tag: Annotated[str, typer.Option()] = DEFAULT_TAG,
):
    """
    **Publish** a manually entered message
    """

    requests.post(
        url,
        data=message.encode(encoding="utf-8"),
        headers={
            "Priority": str(priority),
            "Tags": tag,
        },
    )


@app.command()
def run():
    """
    **Loop** through event checks
    """
    last_heartbeat = date.today() - timedelta(days=1)
    while True:
        for scraper, tag in scrapers:
            if message := scraper():
                publish(message, tag=tag)

        if (today := date.today()) > last_heartbeat:
            publish(f"{today}", priority=1, tag=HEARTBEAT)
            last_heartbeat = today
        break

        sleep(HALF_AN_HOUR)


if __name__ == "__main__":
    app()
