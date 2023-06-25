from math import radians, sin, cos, atan2, sqrt


def distance_formatter(func):
    """ Можно использывать как @distance_formatter """
    def wrapper(lat1, lon1, lat2, lon2):
        distance_in_meters = func(lat1, lon1, lat2, lon2)

        if distance_in_meters >= 1000:
            return f"{round(distance_in_meters / 1000, 2)} км"
        elif distance_in_meters >= 1:
            return f"{distance_in_meters} м"
        return "Обернитесь, вы рядом!"

    return wrapper


def calculate_distance_in_meters(lat1, lon1, lat2, lon2):
    radius = 6371000

    # Формула Винсенти
    a = sin((radians(lat2) - radians(lat1)) / 2) ** 2 + \
        cos(radians(lat1)) * cos(radians(lat2)) * \
        sin((radians(lon2) - radians(lon1)) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return round(distance)
