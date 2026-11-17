ngo_data = [
    {
        "name": "Helping Hands NGO",
        "location": "Tumakuru",
        "food_type": "Vegetarian",
        "capacity": 50
    },
    {
        "name": "Food for All",
        "location": "Bangalore",
        "food_type": "Vegetarian",
        "capacity": 100
    },
    {
        "name": "Care Foundation",
        "location": "Tumakuru",
        "food_type": "Vegan",
        "capacity": 30
    },
    {
        "name": "Sira Sample NGO",
        "location": "Sira",
        "food_type": "Vegetarian",
        "capacity": 60
    }
]


def match_ngos(location, food_type, quantity):

    suitable_ngos = []

    for ngo in ngo_data:

        if (
            ngo["location"].lower() in location.lower()
            and ngo["food_type"] == food_type
            and ngo["capacity"] >= quantity
        ):

            suitable_ngos.append(ngo)

    return suitable_ngos