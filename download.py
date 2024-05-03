from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/home')
def scrape_data():
    url = "https://web.sketchub.in/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Selecting the titles
    titles = soup.select("p.appCard__appname")
    
    # Selecting the images
    images = soup.select("img.appIcon")
    
    # Extracting text from title elements
    app_data = []
    for title, img in zip(titles, images):
        app_data.append({
            'title': title.text.strip(),
            'image_src': img['src']
        })
    
    return jsonify(app_data)

if __name__ == '__main__':
    app.run(debug=True)
