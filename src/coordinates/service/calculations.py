from math import cos, sin, acos, radians, atan2, sqrt
from typing import Tuple, Iterable, Any
from functools import wraps

import numpy as np


# ============================== MATH FUNCTIONS =============================== #

def calculate_distance_1(lat1, lon1, lat2, lon2) -> float:
    """
    cos(d) = sin(φА)·sin(φB) + cos(φА)·cos(φB)·cos(λА − λB),
    где φА и φB — широты, λА, λB — долготы данных пунктов, d — расстояние между пунктами,
    измеряемое в радианах длиной дуги большого круга земного шара.
    Расстояние между пунктами, измеряемое в километрах, определяется по формуле:
    L = d·R,
    где R = 6371 км — средний радиус земного шара.
    """
    R = 6371
    cos_d = sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2))\
             * cos(radians(lon1) - radians(lon2))   # noqa: E127
    d = acos(cos_d)
    return d * R * 1000   # return L


def distance_formatter(func):
    """ Можно использовать как @distance_formatter."""
    @wraps(func)
    def wrapper(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
        distance_in_meters = func(lat1, lon1, lat2, lon2)

        if distance_in_meters >= 1000:
            return f"{round(distance_in_meters / 1000, 2)} км"
        elif distance_in_meters >= 1:
            return f"{distance_in_meters} м"
        return "Обернитесь, вы рядом!"

    return wrapper


def calculate_distance_2(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6_371_000
    # Формула Винсенти
    a = sin((radians(lat2) - radians(lat1)) / 2) ** 2 + \
        cos(radians(lat1)) * cos(radians(lat2)) * \
        sin((radians(lon2) - radians(lon1)) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return round(distance)


# ============================== NUMPY FUNCTIONS =============================== #

def vectorize_queryset(queryset: Iterable) -> Tuple[np.ndarray, np.ndarray]:
    """Make latitude vector and longitude vector out of queryset."""
    return (
        np.array([q.lat for q in queryset], dtype="float32"),
        np.array([q.lon for q in queryset], dtype="float32")
    )


def vectorize_queryset_dict(queryset: Iterable):
    """Make latitude vector and longitude vector out of a mapping obj."""
    return (
        np.array([q['lat'] for q in queryset], dtype="float32"),
        np.array([q['lon'] for q in queryset], dtype="float32")
    )


def calculate_vector_distance(lat1: float, lat2: np.ndarray, lon1: float, lon2: np.ndarray) -> np.ndarray[Any, Any]:
    """
    lat1 and lon1: some user coordinate to compare other coordinate with;
    lat2 and lon2: vectors of all users coordinates.
    """
    R = 6371 * 1000     # Earth radius in meters.
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    cos_d = (np.sin(lat1) * np.sin(lat2)) + ((np.cos(lat1) * np.cos(lat2)) * np.cos(lon1 - lon2))
    return np.arccos(cos_d) * R  # type: ignore
