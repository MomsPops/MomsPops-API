import random
from dataclasses import dataclass
from functools import wraps
from time import perf_counter

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
    # return list(CoordinateManager().all_near(coord1, coords_queryset))


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
    # return list(CoordinateManager().all_near(coord1, coords_queryset))


@time_measure
def test_time_vector(n_samples: int):
    coord1 = Coordinate(random.uniform(-90, 90), random.uniform(-180, 180))
    coords_queryset = [
        Coordinate(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(n_samples)
    ]
    lat2_v, lon2_v = vectorize_queryset(queryset=coords_queryset)
    distances = calculate_vector_distance(
            lat1=coord1.lat,
            lon1=coord1.lon,
            lat2=lat2_v,
            lon2=lon2_v
        )
    return distances
    # return list(CoordinateManager().all_near(coord1, coords_queryset))


# lst1 = test_time_1(10**6)
# lst2 = test_time_2(10**6)
# lst_v = test_time_vector(10**6)

# args = [100, 100, 100.123123, 1012]
# print(coordinates_distance_1(*args))
# print(calculate_distance_2(*args))
# print(
#     calculate_vector_distance(
#     args[0], np.array([args[1]]),
#     args[2], np.array([args[3]])
# )
# )

lat1 = 43.220012
lon1 = 76.931694
lat2 = 43.229381
lon2 = 76.944408
print(calculate_distance_1(lat1, lat2, lon1, lon2))
