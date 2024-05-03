from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/app', methods=['GET'])
def get_apk_data():
    url = "https://apksos.com/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    app_titles = soup.select("div.col-md-9.col-sm-9.apptitle")
    app_icons = soup.select("div.col-md-3.col-sm-3.vcenter")

    apk_data = []
    for app_title, app_icon in zip(app_titles, app_icons):
        apk_name_element = app_title.find("p")
        apk_img_element = app_icon.find("img")
        if apk_name_element and apk_img_element:
            apk_name = apk_name_element.get_text(strip=True)
            apk_img_src = apk_img_element.get("data-original")
            apk_info = {
                "name": apk_name,
                "image_src": apk_img_src
            }
            apk_data.append(apk_info)

    return jsonify(apk_data)

if __name__ == '__main__':
    app.run(debug=True)
