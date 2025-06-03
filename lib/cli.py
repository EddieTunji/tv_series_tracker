import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models import Series, Season, Episode, User, Review, Status
from lib.db import session
from tabulate import tabulate
from colorama import Fore, Style, init
init(autoreset=True)

def greet():
    print(Fore.MAGENTA + Style.BRIGHT + "\n🎬 Welcome to the TV Series Tracker CLI!")
    print(Fore.CYAN + "Track what you watch. Share what you think.\n")

def select_user():
    while True:
        users = session.query(User).all()
        if users:
            print("📺 Existing users:")
            for user in users:
                print(f"- {user.username}")
        else:
            print("No users found. Please create one.")

        choice = input("Enter your username or type 'new' to create one: ").strip()

        if choice.lower() == 'new':
            username = input("Enter new username: ").strip()
            if username:
                user = User(username=username)
                session.add(user)
                session.commit()
                print(f"✅ User '{username}' created.\n")
                return user
            else:
                print("Username cannot be empty.")
        else:
            user = session.query(User).filter_by(username=choice).first()
            if user:
                print(f"✅ Logged in as {user.username}\n")
                return user
            else:
                print("❌ User not found. Try again.")

def list_all_series():
    series = session.query(Series).all()
    if not series:
        print("No series available.")
        return
    data = [(s.id, s.title, s.genre) for s in series]
    print(tabulate(data, headers=["ID", "Title", "Genre"], tablefmt="fancy_grid"))

def view_series_details(user):
    while True:
        series_list = session.query(Series).all()
        if not series_list:
            print("No series to view.")
            return
        list_all_series()
        selection = input("Enter series ID to view details or 'b' to go back: ").strip()
        if selection.lower() == 'b':
            return
        try:
            selected = session.get(Series, int(selection))
        except (ValueError, TypeError):
            selected = None
        if not selected:
            print("Invalid selection.")
            continue

        print(f"\n📺 {selected.title} ({selected.genre})")
        print(f"Description: {selected.description}")

        for season in selected.seasons:
            print(f"  Season {season.season_number}")
            for ep in season.episodes:
                print(f"    - {ep.title} ({ep.duration_mins} mins)")

        status = session.query(Status).filter_by(user_id=user.id, series_id=selected.id).first()
        if status:
            print(f"📌 Your status: {status.watch_status}")

        print("\n📝 Reviews:")
        for r in selected.reviews:
            stars = '⭐' * r.rating
            print(f"{r.user.username}: {stars} ({r.rating}/10) – {r.content}")
        break

def add_review(user):
    while True:
        list_all_series()
        selection = input("Enter series ID to review or 'b' to go back: ").strip()
        if selection.lower() == 'b':
            return
        try:
            selected = session.get(Series, int(selection))
        except (ValueError, TypeError):
            selected = None
        if not selected:
            print("Invalid selection.")
            continue

        rating_input = input("Enter your rating (1–10) or 'b' to cancel: ")
        if rating_input.lower() == 'b':
            return
        try:
            rating = int(rating_input)
            if not 1 <= rating <= 10:
                raise ValueError
        except ValueError:
            print(Fore.RED + "❌ Invalid rating. Must be a number between 1 and 10.")
            continue

        content = input("Write your review or 'b' to cancel: ")
        if content.lower() == 'b':
            return

        review = Review(user=user, series=selected, rating=rating, content=content)
        session.add(review)
        session.commit()
        print("✅ Review added!")
        break

def update_watch_status(user):
    while True:
        list_all_series()
        selection = input("Enter series ID to update status or 'b' to go back: ").strip()
        if selection.lower() == 'b':
            return
        try:
            selected = session.get(Series, int(selection))
        except (ValueError, TypeError):
            selected = None
        if not selected:
            print("Invalid selection.")
            continue

        new_status = input("Enter new status (Watching / Completed / Dropped / Plan to Watch) or 'b' to cancel: ").strip()
        if new_status.lower() == 'b':
            return

        status = session.query(Status).filter_by(user_id=user.id, series_id=selected.id).first()
        if status:
            status.watch_status = new_status.title()
        else:
            status = Status(user=user, series=selected, watch_status=new_status.title())
            session.add(status)

        session.commit()
        print("✅ Status updated!")
        break

def create_series(user):
    title = input("Enter series title: ").strip()
    genre = input("Enter genre: ").strip()
    description = input("Enter description: ").strip()

    if not title or not genre:
        print("❌ Title and Genre are required.")
        return

    new_series = Series(title=title, genre=genre, description=description, user=user)
    session.add(new_series)
    session.commit()
    print(f"✅ '{title}' added.")

    try:
        num_seasons = int(input("How many seasons does this series have? "))
        for s_num in range(1, num_seasons + 1):
            season = Season(series=new_series, season_number=s_num)
            session.add(season)
            session.commit()

            num_episodes = int(input(f"  How many episodes in Season {s_num}? "))
            for e_num in range(1, num_episodes + 1):
                ep_title = input(f"    Title for Episode {e_num}: ").strip()
                ep_duration = input(f"    Duration in minutes for Episode {e_num}: ").strip()
                try:
                    ep_duration = int(ep_duration)
                except ValueError:
                    ep_duration = 30
                episode = Episode(season=season, episode_number=e_num, title=ep_title, duration_mins=ep_duration)
                session.add(episode)
        session.commit()
        print("✅ Seasons and episodes added.")
    except ValueError:
        print("Invalid input. Skipping season/episode creation.")

def add_season_to_series(user):
    user_series = session.query(Series).filter_by(user_id=user.id).all()
    if not user_series:
        print("❌ You haven't created any series.")
        return

    for s in user_series:
        print(f"{s.id}. {s.title}")

    selection = input("Select series ID to add a season to or 'b' to go back: ").strip()
    if selection.lower() == 'b':
        return
    try:
        selected = session.get(Series, int(selection))
    except:
        selected = None

    if not selected or selected.user_id != user.id:
        print("❌ Invalid selection.")
        return

    try:
        season_number = int(input("Enter the new season number: "))
        season = Season(series=selected, season_number=season_number)
        session.add(season)
        session.commit()
        print(f"✅ Season {season_number} added to '{selected.title}'")
    except ValueError:
        print("❌ Invalid season number.")

def add_episode_to_season(user):
    user_series = session.query(Series).filter_by(user_id=user.id).all()
    if not user_series:
        print("❌ You haven't created any series.")
        return

    for s in user_series:
        print(f"{s.id}. {s.title}")

    selection = input("Select series ID to add an episode to or 'b' to go back: ").strip()
    if selection.lower() == 'b':
        return
    try:
        selected_series = session.get(Series, int(selection))
    except:
        selected_series = None

    if not selected_series or selected_series.user_id != user.id:
        print("❌ Invalid selection.")
        return

    if not selected_series.seasons:
        print("⚠️ This series has no seasons yet. Add a season first.")
        return

    for season in selected_series.seasons:
        print(f"{season.id}. Season {season.season_number}")

    s_choice = input("Select season ID to add episode to: ").strip()
    try:
        selected_season = session.get(Season, int(s_choice))
    except:
        selected_season = None

    if not selected_season:
        print("❌ Invalid season selection.")
        return

    ep_title = input("Enter episode title: ").strip()
    try:
        ep_number = int(input("Enter episode number: ").strip())
        ep_duration = int(input("Enter duration (in minutes): ").strip())
    except ValueError:
        print("❌ Invalid input. Episode number and duration must be numbers.")
        return

    new_episode = Episode(
        season=selected_season,
        title=ep_title,
        episode_number=ep_number,
        duration_mins=ep_duration
    )
    session.add(new_episode)
    session.commit()
    print(f"✅ Episode '{ep_title}' added to Season {selected_season.season_number}")


def add_series_to_watchlist(user):
    print("\nAvailable Series:")
    all_series = session.query(Series).all()
    for series in all_series:
        print(f"{series.id}. {series.title}")

    try:
        series_id = int(input("Enter the ID of the series to add to your watchlist: "))
        selected_series = session.query(Series).filter_by(id=series_id).first()

        if not selected_series:
            print("❌ Series not found.")
            return

        existing = session.query(Status).filter_by(user_id=user.id, series_id=selected_series.id).first()
        if existing:
            print("⚠️ This series is already in your watchlist.")
            return

        new_status = Status(user_id=user.id, series_id=selected_series.id, watch_status="Plan to Watch")
        session.add(new_status)
        session.commit()
        print(f"✅ '{selected_series.title}' has been added to your watchlist!")

    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        session.rollback()
        print(f"❌ An error occurred: {e}")

def view_watchlist(user):
    statuses = session.query(Status).filter_by(user_id=user.id).all()
    if not statuses:
        print("\n📭 Your watchlist is empty.")
        return

    data = [(s.series.id, s.series.title, s.watch_status) for s in statuses]
    print("\n👓 Your Watchlist:")
    print(tabulate(data, headers=["Series ID", "Title", "Watch Status"], tablefmt="fancy_grid"))

def remove_series_from_watchlist(user):
    statuses = (
        session.query(Status)
        .join(Series)
        .filter(Status.user_id == user.id)
        .all()
    )

    if not statuses:
        print("\n📭 Your watchlist is empty.")
        return

    print("\n👓 Your Watchlist:")
    for status in statuses:
        print(f"{status.series.id}. {status.series.title} - {status.watch_status}")

    try:
        series_id = int(input("Enter the Series ID to remove from your watchlist: "))
        status = session.query(Status).filter_by(user_id=user.id, series_id=series_id).first()

        if not status:
            print("❌ This series is not in your watchlist.")
            return

        session.delete(status)
        session.commit()
        print(Fore.RED + "🗑️ Deleting series...")
        time.sleep(1)
        print(f"🗑️ '{status.series.title}' has been removed from your watchlist.")

    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        session.rollback()
        print(f"❌ An error occurred: {e}")

def delete_series(user):
    user_series = session.query(Series).filter_by(user_id=user.id).all()
    if not user_series:
        print(Fore.YELLOW + "⚠️ You haven't created any series to delete.")
        return

    for s in user_series:
        print(f"{s.id}. {s.title}")

    selection = input("Select a series ID to delete or 'b' to go back: ").strip()
    if selection.lower() == 'b':
        return

    try:
        selected_series = session.get(Series, int(selection))
    except:
        selected_series = None

    if not selected_series or selected_series.user_id != user.id:
        print("❌ Invalid selection.")
        return

    confirm = input(f"⚠️ Are you sure you want to delete '{selected_series.title}' and all its data? (yes/no): ").strip().lower()
    if confirm == 'yes':
        session.delete(selected_series)
        session.commit()
        print(Fore.RED + "🗑️ Deleting series...")
        time.sleep(1)
        print(f"✅ '{selected_series.title}' has been permanently removed.\n")

    else:
        print("❌ Deletion cancelled.")

def run_cli(user):
    while True:
        print(Fore.LIGHTGREEN_EX + f"\nWhat would you like to do, {user.username}?")
        print(Fore.CYAN + "1.📃 List all series")
        print(Fore.CYAN + "2.🔍 View series details")
        print(Fore.CYAN + "3.✍️ Add a review")
        print(Fore.CYAN + "4.✅ Update watch status")
        print(Fore.CYAN + "5.➕🎬 Create a new series")
        print(Fore.CYAN + "6.📦➕ Add a season to your series")
        print(Fore.CYAN + "7.🎞️➕ Add an episode to your season")
        print(Fore.CYAN + "8.👓 View watchlist")
        print(Fore.CYAN + "9.🎥➕ Add series to watchlist")
        print(Fore.CYAN + "10.🏌🏾 Remove series from watchlist")
        print(Fore.CYAN + "11.🗑️📦 Delete a series you created")
        print(Fore.CYAN + "12.🚪 Exit")

        choice = input(Fore.LIGHTGREEN_EX + "Select an option: ").strip()

        if choice == "1":
            list_all_series()
        elif choice == "2":
            view_series_details(user)
        elif choice == "3":
            add_review(user)
        elif choice == "4":
            update_watch_status(user)
        elif choice == "5":
            create_series(user)
        elif choice == "6":
            add_season_to_series(user)
        elif choice == "7":
            add_episode_to_season(user)
        elif choice == "8":
            view_watchlist(user)
        elif choice == "9":
            add_series_to_watchlist(user)
        elif choice == "10":
            remove_series_from_watchlist(user)
        elif choice == "11":
            delete_series(user)
        elif choice == "12":
            print(Fore.BLUE + "👋 Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number between 1-12.")

if __name__ == "__main__":
    greet()
    user = select_user()
    run_cli(user)
