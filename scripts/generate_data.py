
def generate_activities():
    import requests

    activities = [
        {"name": "Еда"},
        {"name": "Мясо", "parent_id": 1},
        {"name": "Колбаса", "parent_id": 2},
        {"name": "Овощи", "parent_id": 1},
        {"name": "Огурцы", "parent_id": 4},
        {"name": "Фрукты", "parent_id": 1},
        {"name": "Бананы", "parent_id": 6},
        {"name": "Напитки", "parent_id": 1},
        {"name": "Вода", "parent_id": 8},
        {"name": "Газировка", "parent_id": 8},
        {"name": "Электроника"},
        {"name": "Смартфоны", "parent_id": 11},
        {"name": "Айфоны", "parent_id": 12},
        {"name": "Самсунги", "parent_id": 12},
        {"name": "Ноутбуки", "parent_id": 11},
        {"name": "Игровые ноутбуки", "parent_id": 15},
        {"name": "Ультрабуки", "parent_id": 15},
    ]

    for activity in activities:
        response = requests.post("http://localhost:8080/activity/add", json=activity)
        print(f"Added activity: {response.json()}")


def generate_buildings():
    import requests

    buildings = [
        {"city": "Москва", "street": "Ленина", "building_number": "14", "apartments": "офис 1", "latitude": 55.7558, "longitude": 37.6176},
        {"city": "Барнаул", "street": "Советская", "building_number": "7", "apartments": "офис 3", "latitude": 53.3478, "longitude": 83.7784},
        {"city": "Санкт-Петербург", "street": "Невский проспект", "building_number": "28", "apartments": "офис 5", "latitude": 59.9343, "longitude": 30.3351},
        {"city": "Новосибирск", "street": "Красный проспект", "building_number": "45", "apartments": "офис 2", "latitude": 55.0084, "longitude": 82.9357},
        {"city": "Новосибирск", "street": "Красный проспект", "building_number": "45", "apartments": "офис 3", "latitude": 55.0084, "longitude": 82.9357},
    ]

    for building in buildings:
        response = requests.post("http://localhost:8080/building/add", json=building)
        print(f"Added building: {response.json()}")

def generate_organizations():
    import requests

    organizations = [
        {"name": "ООО Ромашка", "phone": ["+7-999-123-45-67", "+7-999-444-55-55"], "building_id": 1, "activity_ids": [3]},
        {"name": "ИП Васильев", "phone": ["+7-999-234-56-78"], "building_id": 2, "activity_ids": [5]},
        {"name": "ЗАО Техно", "phone": ["+7-999-345-67-89"], "building_id": 3, "activity_ids": [13, 14]},
        {"name": "ООО Питание", "phone": ["+7-999-456-78-90"], "building_id": 4, "activity_ids": [9]},
        {"name": "ООО Питаловка", "phone": ["+7-999-456-78-90"], "building_id": 5, "activity_ids": [9]},
    ]

    for organization in organizations:
        response = requests.post("http://localhost:8080/organization/add", json=organization)
        print(f"Added organization: {response.json()}")


if __name__ == "__main__":
    generate_activities()
    generate_buildings()
    generate_organizations()