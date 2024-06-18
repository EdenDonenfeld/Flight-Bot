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
            # entities["Date"] = format_date(entities["Date"])
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

#same code but in a function
def extract_places(text):
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
    from datetime import datetime
    # 1. date could be in a few formats - dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy or without year - dd/mm, dd-mm, dd.mm
    # 2. if only day and month are given, check if possible for current year, if not, check for next year
    # 3. convert the date to the format dd/mm/yyyy
    # 5. conver to datetime object
    # 6. return the datetime object

    date_format = '%d/%m/%Y'

    date = date.replace('-', '/')
    date = date.replace('.', '/')
    parts = date.split('/')
    
    # day-month-year
    if len(parts) == 3:
        if len(parts[2]) == 2:
            # if year is given with 2 digits, add 20 to the beginning (24 => 2024)
            parts[2] = '20' + parts[2]
            date = '/'.join(parts)
        try:
            date_obj = datetime.strptime(date, date_format)
        except ValueError:
            return None
        return date_obj

    # day-month
    if len(parts) == 2:
        parts.append(str(datetime.today().year))
        print(parts)
        date = '/'.join(parts)
        try:
            date_obj = datetime.strptime(date, date_format)
        except ValueError:
            return None
        if date_obj < datetime.today():
            date_obj = date_obj.replace(year=date_obj.year + 1)
        return date_obj


def is_valid_date(day, month, year=2024):
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        day_count_for_month[2] = 29
    print(year, month, day, day_count_for_month[month])
    return (1 <= month <= 12 and 1 <= day <= day_count_for_month[month])

        
def valid_date_check(date):
    from datetime import datetime
    # 1. check if the date is in the past
    # 2. check if the date is in the next 2 years
    # 3. return True if the date is valid, False otherwise

    if date < datetime.today():
        return False
    if date.year > datetime.today().year + 2:
        return False
    return True


def main():
    # For testing purposes
    dates = ['12/12/2022', '12/12/22', '12-12-2022', '12-12-22', '12.12.2022', '12.12.22', '12/12', '12-5', '12.12', '13.13', '29.2.2023', '29.2.2024']
    counter = 1
    for date in dates:
        print(f"Test {counter}")
        print(date)
        date = format_date(date)
        if date:
            print(date)
            print(is_valid_date(date.day, date.month, date.year))
            print(valid_date_check(date))
        else:
            print("Invalid date")
        counter += 1



if __name__ == "__main__":
    main()