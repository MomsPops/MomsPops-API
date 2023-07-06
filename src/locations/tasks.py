from celery import shared_task

from .service.load_data import load_locations, load_cities, load_regions


@shared_task()
def load_locations_task():
    load_locations()


@shared_task()
def load_cities_task():
    load_cities()


@shared_task()
def load_regions_task():
    load_regions()
