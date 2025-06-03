import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
from random import choice, randint
from lib.models import Series, Season, Episode, User, Review, Status
from lib.db import session

fake = Faker()

# Clear old data
session.query(Status).delete()
session.query(Review).delete()
session.query(Episode).delete()
session.query(Season).delete()
session.query(Series).delete()
session.query(User).delete()

# Users
users = [
    User(username="eddie"),
    User(username="jane_doe"),
    User(username="tv_lover92"),
    User(username="admin"),
]
session.add_all(users)
session.commit()

# Series with detailed data
series_data = [
    {
        "title": "Silo",
        "genre": "Sci-Fi",
        "description": "A dystopian future where humanity lives in a giant underground silo."
    },
    {
        "title": "The Witcher",
        "genre": "Fantasy",
        "description": "A monster hunter navigates a brutal world of magic, betrayal, and destiny."
    },
    {
        "title": "Atlanta",
        "genre": "Drama/Comedy",
        "description": "Two cousins navigate the Atlanta rap scene while dealing with real-life struggles."
    },
    {
        "title": "Dark",
        "genre": "Sci-Fi/Thriller",
        "description": "Time travel unravels a small German town’s darkest secrets."
    },
    {
        "title": "Invincible",
        "genre": "Superhero/Animation",
        "description": "A teen discovers his father is the world’s most powerful (and darkest) superhero."
    },
    {
        "title": "Claws",
        "genre": "Crime/Drama",
        "description": "Five manicurists enter the dangerous world of crime and money laundering."
    },
    {
        "title": "The Boys",
        "genre": "Superhero/Satire",
        "description": "A gritty look at corrupt superheroes and the vigilantes who fight them."
    },
    {
        "title": "Big Mouth",
        "genre": "Animation/Comedy",
        "description": "Teenagers experience puberty with the help of crude 'hormone monsters'."
    },
    {
        "title": "You",
        "genre": "Psychological Thriller",
        "description": "A charming bookstore manager turns obsessive and dangerous in the name of love."
    },
    {
        "title": "How I Met Your Mother",
        "genre": "Sitcom",
        "description": "A man recounts the story of how he met the mother of his children to his kids."
    },
]

series_objects = []
for s in series_data:
    new_series = Series(title=s["title"], genre=s["genre"], description=s["description"])
    session.add(new_series)
    session.flush()  # to get the ID
    series_objects.append(new_series)
session.commit()

# Seasons and Episodes
for series in series_objects:
    for season_num in range(1, 3):  # 2 seasons each
        season = Season(series_id=series.id, season_number=season_num)
        session.add(season)
        session.flush()
        for ep_num in range(1, 11):  # 10 episodes per season
            episode = Episode(season_id=season.id, title=f"Episode {ep_num}", duration_mins=45)
            session.add(episode)
session.commit()

# Statuses
statuses = [
    Status(user_id=users[0].id, series_id=series_objects[0].id, watch_status="Watching"),
    Status(user_id=users[1].id, series_id=series_objects[1].id, watch_status="Completed"),
    Status(user_id=users[2].id, series_id=series_objects[2].id, watch_status="Plan to Watch"),
    Status(user_id=users[3].id, series_id=series_objects[3].id, watch_status="Watching"),
    Status(user_id=users[0].id, series_id=series_objects[4].id, watch_status="Dropped"),
    Status(user_id=users[1].id, series_id=series_objects[5].id, watch_status="Watching"),
]
session.add_all(statuses)
session.commit()

# Reviews
reviews = [
    Review(user_id=users[0].id, series_id=series_objects[0].id, rating=8, content="Amazing concept!"),
    Review(user_id=users[1].id, series_id=series_objects[1].id, rating=9, content="Loved the fantasy elements."),
    Review(user_id=users[2].id, series_id=series_objects[2].id, rating=7, content="Weird but intriguing."),
    Review(user_id=users[3].id, series_id=series_objects[3].id, rating=10, content="Best time travel show ever."),
    Review(user_id=users[0].id, series_id=series_objects[4].id, rating=6, content="Started great, lost steam."),
    Review(user_id=users[1].id, series_id=series_objects[5].id, rating=8, content="Underrated crime drama."),
]
session.add_all(reviews)
session.commit()

print("✅ Database seeded successfully!")
