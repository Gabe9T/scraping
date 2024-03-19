import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.opb.org/'
html = requests.get(url)

if html.status_code == 200:
    # Create a BeautifulSoup object from the HTML content of the webpage
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # Find all elements with class 'story-card story-card__vert color_dgray width_full lead_media'
    story_cards = soup.find_all(class_='story-card story-card__vert color_dgray width_full lead_media')

    # Dictionary to store links and their corresponding text
    links_and_texts = {}

    # If story cards are found
    if story_cards:
        # Loop through each story card
        for card in story_cards:
            # Find the link within the story card
            story_link = card.find('a')['href']
            # Join base URL and relative link to get the full link
            full_link = urljoin(url, story_link)
            # Initialize an empty list for each link in the dictionary
            links_and_texts[full_link] = []

    # Iterate over the keys of the dictionary
    for link in links_and_texts.keys():
        # Make a request to the linked page
        story_response = requests.get(link)
        # If the request is successful
        if story_response.status_code == 200:
            print("Fetching article text from:", link)
            # Create a BeautifulSoup object from the HTML content of the linked page
            story_soup = BeautifulSoup(story_response.content, 'html.parser')
            # Find the article body within the linked page
            article_body = story_soup.find('div', class_='article-body')
            # If the article body is found
            if article_body:
                # Find all paragraphs with the specified class within the article body
                article_texts = article_body.find_all('p', class_='article-body__text article-body--padding color_dgray m-none')
                # Loop through each paragraph
                for text in article_texts:
                    # Append the text to the list corresponding to the link in the dictionary
                    links_and_texts[link].append(text.get_text(separator='\n').strip())
                    # Error handling
            else:
                print("Failed to find article text in:", link)
        else:
            print("Failed to retrieve linked page:", story_response.status_code)
else:
    print("Failed to retrieve webpage. Status code:", html.status_code)

# Print the stored links and their corresponding text for verification
for link, text_list in links_and_texts.items():
    print("Link:", link)
    print("Text:")
    for text in text_list:
        print(text)
    print()  # For readability

# to see scrap data
#print(html.text)