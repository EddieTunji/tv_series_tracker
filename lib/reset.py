import os
from lib.db import engine, Base
from lib import seed

# Delete old DB file
if os.path.exists("tv_series.db"):
    os.remove("tv_series.db")
    print("Deleted old tv_series.db")

Base.metadata.create_all(engine)
print("Database reset complete.")