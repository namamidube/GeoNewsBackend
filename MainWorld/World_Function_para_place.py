import spacy
import requests
import re

nlp = spacy.load('en_core_web_lg')

API_KEY = 'f84b15244f7146a88e7823674744588d'

def get_place_info(place_name):
    
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]
    return None


def is_stopword_present(name):
    return any(word.lower() in nlp.Defaults.stop_words for word in name.split())


def extract_most_relevant_place(paragraph):

    paragraph = clean_paragraph1(paragraph)
    
    place_info_list = extract_places_not_in_india(paragraph)

    if not place_info_list:
        paragraph = clean_paragraph2(paragraph)
        place_info_list = extract_places_not_in_india(paragraph)

    if not place_info_list:
        place_info_list = extract_places_not_in_india2(paragraph)

    sorted_places = sorted(place_info_list, key=lambda x: (x[1].get('priority', 0), x[2]))

    return [place[0] for place in sorted_places]


def clean_paragraph1(paragraph):
    """Removes non-alphabetic characters and extra spaces."""
    paragraph = re.sub(r'\b(U\.S\.|US)\b', 'USA', paragraph)
    paragraph = re.sub(r'\bUK\b', 'United Kingdom', paragraph) 

    return paragraph

def clean_paragraph2(paragraph):

    punctuation_marks = r"([.,!?;:/()\"])"  # Excludes '

    # Add spaces around punctuation
    paragraph = re.sub(punctuation_marks, r" \1 ", paragraph)

    # Replace hyphens/dashes with space
    paragraph = re.sub(r"[-–—]", " ", paragraph)

    # Remove apostrophes from contractions (e.g., "it's" → "its")
    paragraph = re.sub(r"'", "", paragraph)

    # Remove extra spaces caused by replacements
    paragraph = re.sub(r"\s+", " ", paragraph).strip()

    words = paragraph.split()
    paragraph = " ".join(word for word in words if any(c.isupper() for c in word) or word.lower() not in nlp.Defaults.stop_words)


    return paragraph


def extract_places_not_in_india(paragraph):
    """Extracts places outside India without fallback."""
    doc = nlp(paragraph)
    print("Extracted entities:", [(ent.text, ent.label_) for ent in doc.ents])
    places = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]

    return filter_places(paragraph, places, only_india=False)


def extract_places_not_in_india2(paragraph):
    """Extract places by processing each word separately."""
    words = paragraph.split()
    place_info_list = []

    for word in words:
        doc = nlp(word)
        places = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        place_info_list.extend(filter_places(paragraph, places, only_india=False))

    return place_info_list


def filter_places(paragraph, places, only_india):
    """Filters places based on whether they are in India or not."""
    place_info_list = []

    for place in places:
        place_name = place.strip()
        place_parts_list = place_name.split()
        place_info = []

        # First, try the full place name
        info = get_place_info(place_name)
        if info:
            place_info.append((place_name, info))

        # If no valid info, check each part separately
        if not info and len(place_parts_list) > 1:
            for part in place_parts_list:
                part = part.strip()
                info = get_place_info(part)
                if info:
                    place_info.append((part, info))

        # Store places with valid details
        for name, details in place_info:
            position = paragraph.find(name)

            if is_stopword_present(name):
                continue

            place_info_list.append((name, details, position))

    return place_info_list



def main():
    print("Place Extractor: Extract relevant places from a paragraph.")
    paragraph = input("Enter the paragraph to extract places: ")
    
    relevant_places = extract_most_relevant_place(paragraph)
    
    if relevant_places:
        print("Extracted places:", relevant_places)
    else:
        print("No relevant places found.")

if __name__ == "__main__":
    main()