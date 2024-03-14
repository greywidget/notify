import bs4
import requests


def scrape_scorp():
    url = "https://stoffercraft.com/products/spoon-scorp"
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form", action="/cart/add")
    option = form.find("option")
    status = "Sold Out" if "disabled" in option.attrs.keys() else "Available"
    price = form.find("span", id="productPrice").text
    return f"OG Scorp: {price}. {status}"


def scrape_paper():
    url = "https://stoffercraft.com/products/honing-paper"
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form", action="/cart/add")
    options = form.find_all("option")
    option = options[0]
    status = "Sold Out" if "disabled" in option.attrs.keys() else "Available"
    price = form.find("span", id="productPrice").text
    return f"Honing Paper: {price}. {status}"
