from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/app/<path:app_id>')
def get_app_info(app_id):
    try:
        # Construct the URL
        url = f"https://www.appbrain.com/app/{app_id}"
        # Requesting the page
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Getting Title
        appTitle = soup.h1.string

        # Getting Second Title
        appSecTitle = soup.select_one("h2.app-short-description").get_text(strip=True)

        # Getting AppIcon
        appIcon = soup.select_one("div.img-wrapper").find("img")["src"]

        # Getting About App
        aboutApp = [element.get_text(strip=True) for element in soup.select("div.col-12.col-sm-6")]

        # Getting App Description
        appDescription = soup.select_one("a.link")["data-contents"].replace('<br>', ' ')

        # Getting List Of Screenshot
        appScreenshot = [img["src"] for img in soup.select("div.swiper-wrapper img")]

        # Getting Table
        appTable = soup.select_one("table.table.table-striped")

        # Extract data from the table
        data = {}
        for row in appTable.find_all("tr"):
            key = row.find("td").text.strip()
            value = row.find("td").find_next_sibling().text.strip()
            data[key] = value

        # Creating response
        response = {
            "app_title": appTitle,
            "second_title": appSecTitle,
            "app_icon": appIcon,
            "about_app": aboutApp,
            "app_description": appDescription,
            "app_screenshot": appScreenshot,
            "app_data": data
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
