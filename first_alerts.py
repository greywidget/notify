import keyring
import requests
import typer
from decouple import config
from keyring.errors import NoKeyringError


def main(message: str):
    try:
        topic = keyring.get_password("ntfy", "topic")
    except NoKeyringError:
        pass

    if not topic:
        topic = config("TOPIC")

    url = f"https://ntfy.sh/{topic}"

    requests.post(
        url,
        data=message.encode(encoding="utf-8"),
        # headers={"Title": "Greywidget Notifications"},
    )


if __name__ == "__main__":
    typer.run(main)
