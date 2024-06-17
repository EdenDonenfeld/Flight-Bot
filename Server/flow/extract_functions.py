import re
APCode = {
        "ישראל": "TLV",
        "יוון": "ATH",
        "תל אביב": "TLV",
        "ניו יורק": "JFK",
        "לוס אנג'לס": "LAX",
        "פריז": "CDG",
        "לונדון": "LHR",
        "ברלין": "TXL",
        "רומא": "FCO",
        "מדריד": "MAD",
        "אמסטרדם": "AMS",
        "פראג": "PRG",
        "בודפשט": "BUD",
        "וינה": "VIE",
        "פרנקפורט": "FRA",
        "מינכן": "MUC",
        "זיריך": "ZRH",
        "קופנהגן": "CPH",
        "אוסלו": "OSL",
        "סטוקהולם": "ARN",
        "הלסינקי": "HEL",
        "ריגה": "RIX",
        "וילנה": "VNO",
        "קייב": "KBP",
        "מוסקבה": "SVO",
        "סנט פטרסבורג": "LED",
        "קראקוב": "KRK",
        "וורשה": "WAW",
        "בוקרשט": "OTP",
        "סופיה": "SOF",
        "פראג": "PRG",
        "וינה": "VIE",
        "זלצבורג": "ZRH",
        "קראקוב": "KRK",
        "פרנקפורט": "FRA",
        "מינכן": "MUC"
    }   

def extract_entities(text, class_label):
    entities = {
        "Origin": None,
        "Destination": None,
        "Date": None,
        "Date2": None
    }
    if class_label == 0:
        entities["Origin"], entities["Destination"] = extract_places(text)
        if extract_dates(text):
            entities["Date"] = extract_dates(text)[0]
        entities["Origin"] = extract_APCode(entities["Origin"])
        entities["Destination"] = extract_APCode(entities["Destination"])
        
    elif class_label == 1:
        entities["Origin"], entities["Destination"] = extract_places(text)
        if extract_dates(text):
            entities["Date"] = extract_dates(text)[0]
    elif class_label == 2:
        return extract_places(text)
    elif class_label == 3:
        return extract_dates(text)
    elif class_label == 4:
        return extract_places(text)
    elif class_label == 5:
        return extract_places(text)
    else:
        return extract_places(text)
    return entities
    
# returns an array of dates in the text format of only with numbers
def extract_dates(text):
    # Corrected date pattern
    date_pattern = r"\d{1,2}[./\-\s]\d{1,2}(?:[./\-\s]\d{2,4})?"

    # Find all matches
    matches = re.findall(date_pattern, text)
    
    # Sort matches by length in descending order
    matches = sorted(matches, key=len, reverse=True)
    
    filtered_dates = []
    seen = set()
    
    for match in matches:
        # Check if the current match is not a substring of any already seen longer date
        if not any(longer_match for longer_match in seen if match in longer_match):
            filtered_dates.append(match)
            seen.add(match)
    
    return filtered_dates

import re


#same code but in a function
def extract_places(text):
    # places = ["ישראל", "יוון", "תל אביב", "ניו יורק", "לוס אנג'לס", "פריז", "לונדון", "ברלין", "רומא", "מדריד", "אמסטרדם", "פראג", "בודפשט", "וינה", "פרנקפורט", "מינכן", "זיריך", "קופנהגן", "אוסלו", "סטוקהולם", "הלסינקי", "ריגה", "וילנה", "קייב", "מוסקבה", "סנט פטרסבורג", "קראקוב", "וורשה", "בוקרשט", "סופיה", "בוקרשט", "בודפשט", "פראג", "וינה", "זלצבורג", "קראקוב", "פרנקפורט", "מינכן", "ברלין", "קולון", "פריז", "לונדון", "מדריד", "ברצלונה", "רומא", "מילאנו", "פירנצה", "וינציה", "פראג", "ברטיסלבה", "בודפשט", "וינה", "זלצבורג", "קראקוב", "פרנקפורט", "מינכן", "ברלין", "קולון"]
    places = list(APCode.keys())
    places_pattern = "|".join(places)

    before_origin = ["מ", "מאת", "מן", "מן ה"]
    before_destination = ["ל", "אל", "לאת", "לכיוון", "לכיוון של", "לכיוון של ה", "לכיוון שלא", "לכיוון שלאת"]

    Origin = None
    Destination = None

    place_matches = re.findall(places_pattern, text)
    # print(place_matches)
    if place_matches:
        for i, place in enumerate(place_matches):
            if len(place_matches) == 2:
                other_place = place_matches[i-1]
            part_to_check = text.split(place)[0]
            first_part_to_check = part_to_check.split(" ")[-1]
            second_part_to_check = part_to_check.split(" ")[-2]
            #check if the parts are in before_origin or before_destination
            if first_part_to_check in before_origin or second_part_to_check in before_origin:
                Origin = place
                if len(place_matches) == 2:
                    Destination = other_place
            elif first_part_to_check in before_destination or second_part_to_check in before_destination:
                Destination = place
                if len(place_matches) == 2:
                    Origin = other_place
        #if didnt find origin or destination set the first place as origin
        if Origin == None:
            Origin = place_matches[0]
        #if didnt find destination set the second place as destination
        if Destination == None and len(place_matches) == 2:
            Destination = place_matches[1]
    else:
        print("No places found")
    return Origin, Destination
    
#function to extract the airport code from the place
def extract_APCode(place):
    return APCode[place] if place in APCode else None  

def format_date(date):
    # 1. date could be in a few formats - dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy or without year - dd/mm, dd-mm, dd.mm
    # 2. if only day and month are given, check if possible for current year, if not, check for next year
    # 3. convert the date to the format dd/mm/yyyy
    # 5. conver to datetime object
    # 6. return the datetime object

