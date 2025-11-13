from geopy.distance import distance

def is_point_in_radius(point: list[float, float], center: list[float, float], radius: float):
    dist = distance(point, center).meters
    return dist <= radius