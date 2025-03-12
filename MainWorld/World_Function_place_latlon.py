from opencage.geocoder import OpenCageGeocode, OpenCageGeocodeError
import logging
import time

def get_location(address):
    key = 'f84b15244f7146a88e7823674744588d'
    geocoder = OpenCageGeocode(key)

    try:
        if not address.strip():
            raise ValueError("The address provided is empty. Please enter a valid location.")

        result = geocoder.geocode(address)
        
        if result:
            first_location = None  # Initialize the first location variable
            country = None

            for res in result:
                if 'components' in res and 'country' in res['components']:
                    res_country = res['components']['country']
                    location = res['geometry']

                    if not first_location:
                        first_location = location
                        country = res_country

            return first_location['lat'], first_location['lng'], country
        else:
            logging.warning(f"No location found for the address: {address}")

    except Exception as e:
        error_message = str(e)
        
        if "invalid API key" in error_message:
            logging.error("Invalid API key. Please check and update it.")
        elif "rate limit exceeded" in error_message:
            logging.warning("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)
            return get_location(address)  # Retry after wait
        elif "timeout" in error_message:
            logging.error("Request timed out. Check network connection.")
        else:
            logging.error(f"Unexpected error: {e}")

    return None, None, None

def main():
    logging.basicConfig(level=logging.INFO)  # Set up logging for info level messages
    address = input("Enter a location to geocode: ")
    
    lat, lon, country = get_location(address)
    
    if lat is not None and lon is not None:
        print(f"Latitude: {lat}, Longitude: {lon}, Country: {country}")
    else:
        print("Location not found or there was an error.")

if __name__ == "__main__":
    main()