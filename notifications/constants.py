# General travel tips
GENERAL_TIPS = [
    {"title": "Respect Local Customs", "body": "Always be mindful of the local customs and traditions."},
    {"title": "Dress Modestly in Public Spaces", "body": "Avoid wearing revealing clothes in public areas."},
    {"title": "Helmet Safety", "body": "Always wear a helmet when riding bikes or scooters."},
    {"title": "Footwear Etiquette", "body": "Remove your shoes before entering temples or homes."},
    {"title": "Public Transport", "body": "Keep small change handy for bus and train fares."},
    {"title": "Wildlife Safety", "body": "Do not feed or disturb animals in national parks."},
]

notification_schema = {
    "type": "event",
    "title": "Event Nearby!",
    "body": "You are close to Galle Fort. Check it out!",
    "timestamp": "2022-02-28T10:00:00Z",
    "data": {
        "eventId": "1234",
        "location": {
            "lat": 6.0328,
            "lon": 80.2170,
            },
        },
    "read": False,
}