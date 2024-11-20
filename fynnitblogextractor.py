import requests
from bs4 import BeautifulSoup
import time

def scrape_fynnit_blog(url, output_file):
    all_posts = []
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Alle Blog-Einträge finden
    blog_entries = soup.find_all('article')
    
    for entry in blog_entries:
        try:
            # Titel extrahieren
            title_element = entry.find('h2', class_='entry-title')
            if title_element:
                title = title_element.get_text().strip()
                article_link = title_element.find('a')['href']
            else:
                continue
            
            # Metadaten extrahieren (Autor und Datum)
            meta = ""
            meta_element = entry.find(['p', 'div'], class_='entry-meta')
            if meta_element:
                meta = meta_element.get_text().strip()
            
            # Vollständigen Artikel abrufen
            article_response = requests.get(article_link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            # Hauptinhalt extrahieren
            content = article_soup.find('div', class_='entry-content')
            if content:
                # Entferne Script- und Style-Tags
                for script in content.find_all(['script', 'style']):
                    script.decompose()
                content = content.get_text(separator='\n').strip()
            else:
                content = "Kein Inhalt verfügbar"
            
            # Formatierter Text für die Ausgabe
            post_text = f"""
=== {title} ===
{meta}

{content}

URL: {article_link}
-------------------
"""
            all_posts.append(post_text)
            print(f"Artikel extrahiert: {title}")
            
            # Kleine Pause zwischen den Requests
            time.sleep(1)
            
        except Exception as e:
            print(f"Fehler beim Verarbeiten eines Artikels: {str(e)}")
            continue
    
    # Alle Artikel in eine Datei schreiben
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_posts))
        
    print(f"\nAlle Artikel wurden in {output_file} gespeichert.")

# Script ausführen
blog_url = "https://fynnit.de/blog/"
output_file = "fynnit_blog_posts.txt"

scrape_fynnit_blog(blog_url, output_file)