from math import cos, sin, acos, atan2, sqrt


def coordinates_distance_1(lat1, lat2, lon1, lon2) -> float:
    """
    cos(d) = sin(φА)·sin(φB) + cos(φА)·cos(φB)·cos(λА − λB),
    где φА и φB — широты, λА, λB — долготы данных пунктов, d — расстояние между пунктами,
    измеряемое в радианах длиной дуги большого круга земного шара.
    Расстояние между пунктами, измеряемое в километрах, определяется по формуле:
    L = d·R,
    где R = 6371 км — средний радиус земного шара.
    """
    R = 6371
    cos_d = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)
    d = acos(cos_d)

    return d * R * 1000   # return L


def distance_formatter(func):
    """ Можно использовать как @distance_formatter """
    def wrapper(lat1, lon1, lat2, lon2):
        distance_in_meters = func(lat1, lon1, lat2, lon2)

        if distance_in_meters >= 1000:
            return f"{round(distance_in_meters / 1000, 2)} км"
        elif distance_in_meters >= 1:
            return f"{distance_in_meters} м"
        return "Обернитесь, вы рядом!"

    return wrapper


def calculate_distance_2(lat1, lon1, lat2, lon2):
    radius = 6371000

    # Формула Винсенти
    a = sin((lat2 - lat1) / 2) / 2 ** 2 + \
        cos(lat1) * cos(lat2) * \
        sin((lon2 - lon1) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return round(distance)
