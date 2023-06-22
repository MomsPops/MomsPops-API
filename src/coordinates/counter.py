from math import cos, sin, acos


def coordinates_distance(lat1, lat2, lon1, lon2) -> float:
    """
    cos(d) = sin(φА)·sin(φB) + cos(φА)·cos(φB)·cos(λА − λB),

    где φА и φB — широты, λА, λB — долготы данных пунктов, d — расстояние между пунктами, измеряемое в радианах длиной дуги большого круга земного шара.
    Расстояние между пунктами, измеряемое в километрах, определяется по формуле:

    L = d·R,

    где R = 6371 км — средний радиус земного шара.
    """
    R = 6371
    """Function calculates vector length of the coordinates."""
    cos_d = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)
    d = acos(cos_d)

    return d * R    # return L
