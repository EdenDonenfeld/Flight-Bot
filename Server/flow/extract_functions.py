import re
from typing import Tuple, Optional

APCode = {
        "ישראל": "TLV",
        "יוון": "ATH",
        "תל אביב": "TLV",
        "ניו יורק": "JFK",
        "לוס אנגלס": "LAX",
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

def correctDateOrder(date1, date2):
    from datetime import datetime
    date_format = '%d/%m/%Y'
    date1_obj = datetime.strptime(date1, date_format)
    date2_obj = datetime.strptime(date2, date_format)
    if date1_obj > date2_obj:
        return date2, date1
    return date1, date2


def extract_entities(text, class_label):
    entities = {
        "Origin": None,
        "Destination": None,
        "Date": None,
        "Date2": None
    }
    if class_label == 0 or class_label == 1:
        entities["Origin"], entities["Destination"] = extract_places(text)
        if extract_dates(text):
            entities["Date"] = extract_dates(text)[0]
            entities["Date"] = format_date(entities["Date"])
        if len(extract_dates(text)) > 1:
            entities["Date2"] = extract_dates(text)[1]
            entities["Date2"] = format_date(entities["Date2"])
            entities["Date"], entities["Date2"] = correctDateOrder(entities["Date"], entities["Date2"])
        entities["Origin"] = extract_APCode(entities["Origin"])
        entities["Destination"] = extract_APCode(entities["Destination"])
        # If the origin and destination are the same, set the origin to TLV
        if entities["Origin"] == entities["Destination"]:
            entities["Origin"] = "TLV"
        
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
    #remove all the special characters from the text
    text = re.sub(r'[^א-תa-zA-Z0-9\s]', '', text)
    words = text.split(" ")

    places = list(APCode.keys())

    before_origin = ["מ", "מאת", "מן", "מן ה"]
    before_destination = ["ל", "אל", "לאת", "לכיוון", "לכיוון של", "לכיוון של ה", "לכיוון שלא", "לכיוון שלאת"]

    Origin = None
    Destination = None

    # print(f"Debug: Text after preprocessing: {text}")
    # print(f"Debug: Words: {words}")
    # print(f"Debug: Available places: {places}")

    i = 0
    while i < len(words):
        # Check for two-word locations
        if i < len(words) - 1:
            two_word_phrase = words[i] + " " + words[i+1]
            closest_match = find_closest_match(two_word_phrase, places)
            # print(f"Debug: Checking two-word phrase: {two_word_phrase}")
            # print(f"Debug: Closest match: {closest_match}")
            if closest_match:
                if i > 0:
                    prev_word = words[i-1]
                    if prev_word in before_origin:
                        Origin = closest_match
                    elif prev_word in before_destination:
                        Destination = closest_match
                
                if Origin is None:
                    Origin = closest_match
                elif Destination is None and closest_match != Origin:
                    Destination = closest_match
                
                i += 2
                continue

        # Check for single-word locations
        closest_match = find_closest_match(words[i], places)
        # print(f"Debug: Checking single word: {words[i]}")
        # print(f"Debug: Closest match: {closest_match}")
        if closest_match:
            if i > 0:
                prev_word = words[i-1]
                if prev_word in before_origin:
                    Origin = closest_match
                elif prev_word in before_destination:
                    Destination = closest_match
            
            if Origin is None:
                Origin = closest_match
            elif Destination is None and closest_match != Origin:
                Destination = closest_match

        i += 1

    # print(f"Debug: Final Origin: {Origin}")
    # print(f"Debug: Final Destination: {Destination}")
    return Origin, Destination
    
#function to extract the airport code from the place
def extract_APCode(place):
    return APCode[place] if place in APCode else None  

def format_date(date: str) -> str:
    from datetime import datetime
    # 1. date could be in a few formats - dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy or without year - dd/mm, dd-mm, dd.mm
    # 2. if only day and month are given, check if possible for current year, if not, check for next year
    # 3. convert the date to the format dd/mm/yyyy
    # 5. convert to datetime object
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
        date_string = date_obj.strftime(date_format)
        return date_string

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
        # return the date as a string in the format dd/mm/yyyy
        date_string = date_obj.strftime(date_format)
        return date_string


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

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_closest_match(phrase: str, candidates: list, threshold: int = 1) -> Optional[str]:
    if phrase[0] == 'מ' or phrase[0] == 'ל':
        phrase = phrase[1:]
    closest_match = None
    min_distance = float('inf')
    
    for candidate in candidates:
        distance = levenshtein_distance(phrase, candidate)
        if distance < min_distance and distance <= threshold:
            min_distance = distance
            closest_match = candidate
    
    return closest_match

def main():
    test_cases = [
        {
            "text": "אני רוצה להזמין כרטיס טיסה מניו יורק ללוס אנג'לס ב30.5.24",
            "expected": ("ניו יורק", "לוס אנגלס")
        },
        {
            "text": "טיסה מתל אביב לפריז ב-15.7.2024",
            "expected": ("תל אביב", "פריז")
        },
        {
            "text": "אני מעוניין לטוס מלונדון לברלין",
            "expected": ("לונדון", "ברלין")
        },
        {
            "text": "האם יש טיסות זולות מאמסטרדם לרומא?",
            "expected": ("אמסטרדם", "רומא")
        },
        {
            "text": "מחפש טיסה מת''א למדריד בחודש הבא",
            "expected": ("תל אביב", "מדריד")
        },
        {
            "text": "טיסה מישראל ליוון ב-1.8",
            "expected": ("ישראל", "יוון")
        },
        {
            "text": "אני צריך לטוס מניו-יורק לתל-אביב בדחיפות",
            "expected": ("ניו יורק", "תל אביב")
        },
        {
            "text": "יש לי פגישה בפרנקפורט, אני טס מוינה",
            "expected": ("וינה", "פרנקפורט")
        },
        {
            "text": "אני רוצה לטוס ממוסקווה לסנט פטרסבורג",
            "expected": ("מוסקבה", "סנט פטרסבורג")
        },
        {
            "text": "תזמין לי טיסה מקופנהגן לשטוקהולם",
            "expected": ("קופנהגן", "סטוקהולם")
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        text = test_case["text"]
        expected = test_case["expected"]
        result = extract_places(text)
        
        print(f"Test case {i}:")
        print(f"Input: {text}")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        
        if result == expected:
            print("PASSED")
        else:
            print("FAILED")
        print()



if __name__ == "__main__":
    main()