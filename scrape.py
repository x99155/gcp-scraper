import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
import datetime
import time

def scrape_afrik():
    global id_counter

    url = 'https://www.afrik.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Trouver tous les articles
    articles = soup.find_all('div', {'class': 'td_module_mob_1 td_module_wrap td-animation-stack td-meta-info-hide'})

    # Initialiser une liste pour stocker les informations des articles
    articles_info = []

    # Extraire les informations du dernier article publié s'il existe
    if articles:
        latest_article = articles[0]
        link = latest_article.find('a', class_='td-image-wrap')['href']
        image_url = latest_article.find('img', class_='entry-thumb')['src']
        title = latest_article.find('h1', class_='entry-title td-module-title').get_text(strip=True)
        description = latest_article.find('div', class_='td-excerpt').get_text(strip=True)
        
        # Utiliser l'horodatage actuel en millisecondes pour générer un identifiant unique
        unique_id = int(time.time() * 1000)
        article_id = unique_id

        # Stocker ces informations dans le dictionnaire
        article_info = {
            'id': article_id,
            'link': link,
            'image_url': image_url,
            'title': title,
            'description': description,
            'date': datetime.datetime.utcnow().isoformat()
        }

        # Ajouter l'article à la liste
        articles_info.append(article_info)
    else:
        print("Aucun article trouvé")
    
    return articles_info

def store_in_bigquery(articles):
    client = bigquery.Client()
    table_id = 'pro-habitat-424316-b7.gcp_afrikcom.articles'
    errors = client.insert_rows_json(table_id, articles)
    if errors:
        print(f'Encountered errors while inserting rows: {errors}')
    else:
        print(f'Successfully inserted {len(articles)} rows.')

if __name__ == '__main__':
    articles = scrape_afrik()
    if articles:  # Ensure there are articles to store
        store_in_bigquery(articles)
    else:
        print('No articles to store.')


