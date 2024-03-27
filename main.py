from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_sitemap(url):
    def extract_content(url):
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, 'html.parser')
            
            # Extracting title
            title_tag = soup.find('h1', class_='m-none color_dgray article-header__headline p_bottom-xxs')
            title = title_tag.text.strip() if title_tag else None
            
            # Extracting text
            text_tags = soup.find_all('p', class_='article-body__text article-body--padding color_dgray m-none')
            text = '\n'.join([tag.text.strip() for tag in text_tags]) if text_tags else None
            
            return {'title': title, 'text': text}
        else:
            print("Failed to retrieve linked page:", html.status_code)
            return {'title': None, 'text': None}

    html = requests.get(url)
    data = []

    if html.status_code == 200:
        soup = BeautifulSoup(html.content, 'xml')  # Use 'xml' parser for sitemap.xml
        loc_tags = soup.find_all('loc')

        for loc_tag in loc_tags:
            loc = loc_tag.text.strip()
            # Check if URL is from opb.org/article domain
            if 'https://www.opb.org/article/' in loc:
                content = extract_content(loc)
                data.append({'link': loc, 'title': content['title'], 'text': content['text']})
    else:
        print("Failed to retrieve sitemap. Status code:", html.status_code)

    return data

@app.route('/')
def index():
    sitemap_url = 'https://www.opb.org/arc/outboundfeeds/news-sitemap/?outputType=xml'
    data = scrape_sitemap(sitemap_url)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True) 
