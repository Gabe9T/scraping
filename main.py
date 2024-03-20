from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_website(url):
    html = requests.get(url)
    data = []

    if html.status_code == 200:
        soup = BeautifulSoup(html.content, 'html.parser')
        story_cards = soup.find_all(class_='story-card story-card__vert color_dgray width_full lead_media')

        if story_cards:
            for card in story_cards:
                story_link = card.find('a')['href']
                full_link = urljoin(url, story_link)
                story_response = requests.get(full_link)
                if story_response.status_code == 200:
                    story_soup = BeautifulSoup(story_response.content, 'html.parser')
                    # Extracting h1 tag
                    h1_tag = story_soup.find('h1', class_='m-none color_dgray article-header__headline p_bottom-xxs')
                    if h1_tag:
                        h1_text = h1_tag.text.strip()
                    else:
                        h1_text = None
                    
                    # Extracting article text
                    article_texts = story_soup.find_all('p', class_='article-body__text article-body--padding color_dgray m-none')
                    formatted_text = '\n'.join([text.get_text(strip=True) for text in article_texts])
                    
                    # Storing data as a dictionary
                    data.append({
                        'link': full_link,
                        'title': h1_text,
                        'text': formatted_text
                    })
                else:
                    print("Failed to retrieve linked page:", story_response.status_code)
    else:
        print("Failed to retrieve webpage. Status code:", html.status_code)

    return data

@app.route('/')
def index():
    url = 'https://www.opb.org/'
    data = scrape_website(url)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)