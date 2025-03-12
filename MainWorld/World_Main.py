from World_Function_para_place import extract_most_relevant_place
from World_Function_place_latlon import get_location
from DB import insert_cluster,insert_article,insert_general_article
from World_Fetch_article import fetch_articles,process_articles


def main():
    print("Fetching articles...")
    articles = fetch_articles()

    if not articles:
        return

    valid_articles = process_articles(articles)

    if not valid_articles:
        return

    for article in valid_articles:
        print("\n" + "="*50 + "\n")
        title = article.get("title", "N/A")
        hi_title = article.get("hi_title", "N/A")
        summary = article.get("description", "N/A")
        hi_description = article.get("hi_description", "N/A")
        source_url = article.get("link", "N/A")
        published_date = article.get("pubDate", "N/A")
        category = article.get("category", "uncategorized")
        image= article.get("image_url", "N/A")

        print(published_date)
        if hi_title != "N/A" and hi_description != "N/A":
            final_description = f"{hi_title}. {hi_description}"
        else:
            final_description = f"{title}. {summary}"
        
        '''print()
        for key, value in article.items():
            print(f"{key}: {value}")
        print()'''

        print(final_description)

        place_names = extract_most_relevant_place(final_description)

        if place_names:
            valid_place = None
            for place_name in place_names:
                print(f"Checking place: {place_name}")
                lat, lon, country = get_location(place_name)
                if lat is not None and lon is not None:
                    print(f"Valid location found: {place_name} ({lat}, {lon})")
                    insert_cluster(place_name, lat, lon, country)
                    insert_article(title, summary, source_url, published_date, place_name, category,image, country)
                    print("Title:",title)
                    print("summary:",summary)
                    valid_place = True
                    break  # Stop once a valid location is found

            # If no valid place is found after checking all possible places, insert into general_article
            if not valid_place:
                print("No valid location found")
                insert_general_article(title, summary, source_url, published_date, category,image)
                print("Title:",title)
                print("summary:",summary)
        else:
            print("No location found.")
            insert_general_article(title, summary, source_url, published_date, category,image)
            print("Title:",title)
            print("summary:",summary)



'''def main():
    print("Fetching articles...")
    articles = fetch_articles()

    if not articles:
        return

    valid_articles = process_articles(articles)

    if not valid_articles:
        return

    for article in valid_articles:

        title = article.get("title", "N/A")
        summary = article.get("description", "N/A")
        hi_description = article.get("hi_description", "N/A")
        source_url = article.get("link", "N/A")
        published_date = article.get("pubDate", "N/A")
        category = article.get("category", "uncategorized")
        print(summary)
        if hi_description != "N/A":
            description = hi_description  # Use the Hindi description if it's not "N/A"
        else:
            description = summary
        place_name = extract_most_relevant_place(description)
        if place_name:
            address = place_name
            print(address)
            lat, lon = get_location(address)
            if lat is not None and lon is not None:
                print(lat, lon)
                insert_cluster(address, lat, lon)

                insert_article(title, summary, source_url, published_date, place_name, category)

            else:
                print("Location not found or not in India.")
                insert_general_article(title, summary, source_url, published_date, category)
        else:
            print("No location found.")
            insert_general_article(title, summary, source_url, published_date, category)
        
    
    
''' 

if __name__ == "__main__":
    main()
