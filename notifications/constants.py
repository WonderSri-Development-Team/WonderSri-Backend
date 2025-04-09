GENERAL_TIPS = [
    {"title": "Respect Local Customs", "body": "Always be mindful of the local customs and traditions."},
    {"title": "Dress Modestly in Public Spaces", "body": "Avoid wearing revealing clothes in public areas."},
    {"title": "Helmet Safety", "body": "Always wear a helmet when riding bikes or scooters."},
    {"title": "Footwear Etiquette", "body": "Remove your shoes before entering temples or homes."},
    {"title": "Public Transport", "body": "Keep small change handy for bus and train fares."},
    {"title": "Wildlife Safety", "body": "Do not feed or disturb animals in national parks."},
]

NOTIFICATION_SCHEMA = {
    "type": "str",
    "title": "str",
    "body": "str",
    "timestamp": "datetime",
    "data": {
        "eventId": "int",
        "location": {
            "lat": "float",
            "lon": "float",
            },
        },
    "read": "bool",
}