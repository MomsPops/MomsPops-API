from math import radians, sin, cos, atan2, sqrt


def calculate_distance(geo1: str, geo2: str) -> str:
    lat1, lon1 = geo1.split(', ')
    lat2, lon2 = geo2.split(', ')

    lat1 = float(lat1.replace(',', '.'))
    lon1 = float(lon1.replace(',', '.'))
    lat2 = float(lat2.replace(',', '.'))
    lon2 = float(lon2.replace(',', '.'))

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    radius = 6371000

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула Винсенти
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    if distance >= 1000:
        distance /= 1000
        distance = round(distance, 2)
        return f"{distance} км"
    elif distance >= 1:
        distance = round(distance)
        return f"{distance} м"

    return "Обернитесь, вы рядом!"
