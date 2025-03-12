import requests
import certifi
from langdetect import detect, DetectorFactory
from googletrans import Translator

API_URL = "https://newsdata.io/api/1/news"
API_KEY = "pub_5956929872324be1c48d5790c90c0fa9abfe5"

translator = Translator()


def fetch_articles():
    params = {
        "apikey": API_KEY,
        "language": "en,hi",
    }
    try:
        response = requests.get(API_URL, params=params, verify=certifi.where())
        response.raise_for_status()

        articles = response.json().get("results", [])

        if not articles:
            print("No articles found. Exiting.")
            return []

        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
        return []


def translate_if_hindi(text):
    """Translate the text from Hindi to English using Google Translate."""
    if text:
        try:
            translated = translator.translate(text, src='hi', dest='en')
            return translated.text
        except Exception as e:
            print(f"Translation error: {e}")
    return text


def check_language(article):
    """Check if the title is in English or Hindi."""
    try:
        title = article.get("title", "")
        if title:
            detected_title_lang = detect(title)
            if detected_title_lang not in ["en", "hi"]:
                print(f"Skipping article. Detected language - Title: {detected_title_lang}")
                return False
        return True
    except Exception as e:
        print(f"Language detection error: {e}")
        return False
    

def validate_article(article):
    """Validate an article and translate if the language is Hindi."""
    if not article.get("title") or not article.get("description"):
        print("Skipping invalid article with missing fields.")
        return None 

    if not check_language(article):
        print("Skipping invalid article because of language.")
        return None
    
    if article.get("language") == "hindi":
        article["hi_title"] = translate_if_hindi(article["title"])
        article["hi_description"] = translate_if_hindi(article["description"])

    return article 


def process_articles(articles):
    valid_articles = []
    for article in articles:
        #print(article.get("language"))
        valid_article = validate_article(article)
        if valid_article:
            valid_articles.append(valid_article)

    if not valid_articles:
        print("No valid articles found.")
        return []

    return valid_articles


def print_article_details(article):
    """Print selected details of the article."""
    
    title = article.get("title", "N/A")
    hi_title = article.get("hi_title", "N/A")
    description = article.get("description", "N/A")
    hi_description = article.get("hi_description", "N/A")   
    source_url = article.get("link", "N/A")
    published_date = article.get("pubDate", "N/A")
    category = article.get("category", "uncategorized") 
    
    print(f"Title: {title}")
    print(f"hi_Title: {hi_title}")
    print(f"Summary: {description}")
    print(f"hi_Summary: {hi_description}")
    print(f"Source URL: {source_url}")
    print(f"Published Date: {published_date}")
    print(f"Category: {category}")
    print("-" * 80)

'''
def main():
    print("Fetching articles...")
    articles = fetch_articles()

    if not articles:
        return

    valid_articles = process_articles(articles)

    if not valid_articles:
        return

    for article in valid_articles:
        print_article_details(article)


if __name__ == "__main__":
    main()
    '''