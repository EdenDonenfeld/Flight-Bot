from typing import Dict, List, Tuple

def levenshtein_distance(a: str, b: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    matrix = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        matrix[i][0] = i
    for j in range(len(b) + 1):
        matrix[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,   # Deletion
                               matrix[i][j - 1] + 1,   # Insertion
                               matrix[i - 1][j - 1] + cost)  # Substitution
    return matrix[len(a)][len(b)]

def find_closest_city(text: str, valid_cities: List[str], max_distance: int = 2) -> str:
    """Find the closest city from valid_cities to the text based on Levenshtein distance."""
    text = text.strip()
    closest_city = None
    min_distance = max_distance + 1  # Set to higher than max_distance initially
    
    for city in valid_cities:
        distance = levenshtein_distance(text, city)
        if distance < min_distance:
            min_distance = distance
            closest_city = city
            
    return closest_city if min_distance <= max_distance else text

def correct_trip_info(trip_info: Dict[str, str], valid_cities: List[str], max_distance: int = 2) -> Dict[str, str]:
    """Correct origin and destination in trip_info dictionary based on valid_cities."""
    corrected_info = {
        'Origin': find_closest_city(trip_info.get('Origin', ''), valid_cities, max_distance),
        'Destination': find_closest_city(trip_info.get('Destination', ''), valid_cities, max_distance),
        'Date': trip_info.get('Date', ''),
        'Date2': trip_info.get('Date2', ''),
    }
    return corrected_info

# Example usage
valid_cities = ['לוס אנג\'לס', 'ניו יורק', 'שיקגו', 'מיאמי']
trip_info = {
    'Origin': 'לןס אנגלס',  # Example with typo
    'Destination': 'ניו יורק',
    'Date': '2024-09-01',
    'Date2': '2024-09-15'
}

corrected_trip_info = correct_trip_info(trip_info, valid_cities)
print(corrected_trip_info)

# Output will show the corrected origin and destination if there are any typos
