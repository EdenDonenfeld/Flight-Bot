import re
from typing import Tuple, Optional

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
                    if prev_word in before_origin or words[i][0] in before_origin:
                        Origin = closest_match
                    elif prev_word in before_destination or words[i][0] in before_destination:
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
                if prev_word in before_origin or words[i][0] in before_origin:
                    Origin = closest_match
                elif prev_word in before_destination or words[i][0] in before_destination:
                    Destination = closest_match
            
            if Origin is None:
                Origin = closest_match
            elif Destination is None and closest_match != Origin:
                Destination = closest_match

        i += 1

    # print(f"Debug: Final Origin: {Origin}")
    # print(f"Debug: Final Destination: {Destination}")
    return Origin, Destination

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
    if len(phrase.split(" ")) == 1:
        if phrase[0] == 'מ' or phrase[0] == 'ל':
            phrase = phrase[1:]
    if len(phrase.split(" ")) == 2:
        if phrase[0][0] == 'מ' or phrase[0][0] == 'ל':
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
            "text": "אני רוצה להזמין כרטיס טיסה ללוס אנג'לס מניו יורק ב30.5.24",
            "expected": ("ניו יורק", "לוס אנגלס")
        }
        # {
        #     "text": "טיסה מתל אביב לפריז ב-15.7.2024",
        #     "expected": ("תל אביב", "פריז")
        # },
        # {
        #     "text": "אני מעוניין לטוס מלונדון לברלין",
        #     "expected": ("לונדון", "ברלין")
        # },
        # {
        #     "text": "האם יש טיסות זולות מאמסטרדם לרומא?",
        #     "expected": ("אמסטרדם", "רומא")
        # },
        # {
        #     "text": "מחפש טיסה מת''א למדריד בחודש הבא",
        #     "expected": ("תל אביב", "מדריד")
        # },
        # {
        #     "text": "טיסה מישראל ליוון ב-1.8",
        #     "expected": ("ישראל", "יוון")
        # },
        # {
        #     "text": "אני צריך לטוס מניו-יורק לתל-אביב בדחיפות",
        #     "expected": ("ניו יורק", "תל אביב")
        # },
        # {
        #     "text": "יש לי פגישה בפרנקפורט, אני טס מוינה",
        #     "expected": ("וינה", "פרנקפורט")
        # },
        # {
        #     "text": "אני רוצה לטוס ממוסקווה לסנט פטרסבורג",
        #     "expected": ("מוסקבה", "סנט פטרסבורג")
        # },
        # {
        #     "text": "תזמין לי טיסה מקופנהגן לשטוקהולם",
        #     "expected": ("קופנהגן", "סטוקהולם")
        # }
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

if __name__ == "__main__":
    main()