import random
from dataclasses import dataclass
from functools import wraps
from time import perf_counter

# import numpy as np

from coordinates.service.calculations import (
    vectorize_queryset,
    calculate_vector_distance,
    calculate_distance_1,
    calculate_distance_2
)


def time_measure(func):
    @wraps(func)
    def inner(*args, **kwargs):
        time0 = perf_counter()
        res = func(*args, **kwargs)
        time_worked = perf_counter() - time0
        kwargs_string = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        args_string = ", ".join(str(i) for i in args)
        print(f"Time for `{func.__name__}`({args_string}, {kwargs_string}): {time_worked} sec")
        return res
    return inner


class CoordinateManager:
    distance_needed: float = 400_000  # in meters

    def all_near(self, user_coordinate, queryset) -> filter:
        def is_near(coord) -> bool:
            distance = calculate_distance_1(
                lat1=coord.lat,
                lat2=user_coordinate.lat,
                lon1=coord.lon,
                lon2=user_coordinate.lon
            )
            return distance <= self.distance_needed

        return filter(
            is_near,
            queryset
        )


@dataclass
class Coordinate:
    lat: float
    lon: float


@time_measure
def test_time_1(n_samples: int):
    coord1 = Coordinate(random.uniform(-90, 90), random.uniform(-180, 180))
    coords_queryset = [
        Coordinate(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(n_samples)
    ]

    distances = [
        calculate_distance_1(
            lat1=coord1.lat,
            lon1=coord1.lon,
            lat2=c.lat,
            lon2=c.lon
        )
        for c in coords_queryset
    ]
    return distances


@time_measure
def test_time_2(n_samples: int):
    coord1 = Coordinate(random.uniform(-90, 90), random.uniform(-180, 180))
    coords_queryset = [
        Coordinate(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(n_samples)
    ]

    distances = [
        calculate_distance_2(
            lat1=coord1.lat,
            lon1=coord1.lon,
            lat2=c.lat,
            lon2=c.lon
        )
        for c in coords_queryset
    ]
    return distances


@time_measure
def test_time_vector(n_samples: int):
    coord1 = Coordinate(random.uniform(-90, 90), random.uniform(-180, 180))
    coords_queryset = [
        Coordinate(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(n_samples)
    ]
    lat2_v, lon2_v = vectorize_queryset(queryset=coords_queryset)
    distances = calculate_vector_distance(lat1=coord1.lat, lon1=coord1.lon, lat2=lat2_v, lon2=lon2_v)
    return distances


lst1 = test_time_1(10**6)
lst2 = test_time_2(10**6)
lst_v = test_time_vector(10**6)

# kwargs = {
#     "lat1": 100,
#     "lon1": 100,
#     "lat2": 101,
#     "lon2": 101
# }
# print(calculate_distance_1(**kwargs))
# print(calculate_distance_2(**kwargs))
# print(
#     calculate_vector_distance(
#         lat1=100,
#         lon1=100,
#         lat2=np.array([101]),
#         lon2=np.array([101])
#     )
# )
