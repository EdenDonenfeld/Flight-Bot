import dateparser

def parse_hebrew_date(hebrew_date):
    parsed_date = dateparser.parse(hebrew_date, languages=['he'])
    return parsed_date


texts = [
    "מחר",
    "היום",
    "ב-5 לאוגוסט",
    "ב-5 לאוגוסט 2021"
]

for text in texts:
    print(f"Input: {text}, Parsed Date: {parse_hebrew_date(text)}")
