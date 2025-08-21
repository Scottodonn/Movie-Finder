from dotenv import load_dotenv
import os
from tmdbv3api import TMDb
from tmdbv3api import Search, Person
import time


load_dotenv()


TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not found in environment variables. Please check your .env file")


tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY

search = Search()
person_api = Person()


def main():
    while True:
        print("====== MOVIE FINDER ======")

        actor = str(input("Please enter an actor/actress (q to quit): ")).strip().lower()

        if actor == 'q':
            print("Goodbye!")
            break

        if not actor.replace(" ", "").isalpha():
            print("Please enter a valid actor!")
            continue

        print(f"You entered:  {actor}")
        time.sleep(1)
        print(f"Searching for movies with {actor}...")
        time.sleep(3)
        print("Movies found:")
        find_movie(actor)

        # Ask if user wants to search again
        while True:
            end_choice = input("Would you like to search movies for another actor? (Y/N): ").strip().lower()
            if end_choice == 'y':
                break  # Break out of the inner loop to continue the main loop
            elif end_choice == 'n':
                print("Goodbye!")
                return  # Exit the function completely
            else:
                print("Please enter Y or N!")


def find_movie(actor):
    actor_results = search.people(actor)

    if not actor_results:
        print("No actor found with that name!")
    else:
        person_id = actor_results[0].id
        movies = person_api.movie_credits(person_id)['cast']
        movies = sorted(movies, key=lambda x: x.get('release_date', ''), reverse=True)
        if not movies:
            print(f"No movies found for {actor}! ")
        else:
            for movie in movies:
                print(movie['title'])
                print("                  ")


if __name__ == '__main__':
    main()