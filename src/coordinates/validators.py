from django.core.exceptions import ValidationError


def validate_latitude(lat: float) -> float:
    """Latitude is specified in degrees within the range [-90, 90]."""
    if -90 <= lat <= 90:
        return lat
    else:
        raise ValidationError(f"Latitude value {lat} is not in range [-90; 90]")


def validate_longitude(lon: float) -> float:
    """Longitude is specified in degrees within the range [-180, 180)."""
    if -180 <= lon < 180:
        return lon
    else:
        raise ValidationError(f"Longitude value {lon} is not in range [-180; 180)")
