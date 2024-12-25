import joblib
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

feature_matrix, combined_df = joblib.load(r"D:\Coding\Code\Python\ML\IMDB Project\Model Bulding\movie_feature_model.pkl")
print("Loaded")

actors_df = pd.read_csv(r"D:\Coding\Code\Python\ML\Data\IMDB\Cleaned Data\FinalActorBasedRecomendation.csv")  # Load the actor-based data into a DataFrame
directors_df = pd.read_csv(r"D:\Coding\Code\Python\ML\Data\IMDB\Cleaned Data\FinalDirectorBasedRecomendation.csv")  # Load the director-based data into a DataFrame
genres_df = pd.read_csv(r"D:\Coding\Code\Python\ML\Data\IMDB\Cleaned Data\FinalGenreBasedRecomendation.csv")  # Load the genre-based data into a DataFrame
popularity_df = pd.read_csv(r"D:\Coding\Code\Python\ML\Data\IMDB\Cleaned Data\FinalPopularityBasedRecomendation.csv")  # Load the popularity-based data into a DataFrame
print("Loaded")


def get_movie_details(tconst):
    movie_name = genres_df[genres_df['tconst'] == tconst]['primaryTitle'].values

    # Extract actors for the given tconst (movie ID) by filtering the actors DataFrame
    movie_actors = actors_df[actors_df['tconst'] == tconst]['primaryName'].tolist()
    movie_directors = directors_df[directors_df['tconst'] == tconst]['primaryName'].tolist()

    # Extract genres for the given tconst (movie ID) by filtering the genres DataFrame
    movie_genres = genres_df[genres_df['tconst'] == tconst]['genres'].values
    movie_genres = movie_genres[0] if len(movie_genres) > 0 else "Unknown"

    # Extract average rating and number of votes for the movie by filtering the popularity DataFrame
    movie_rating = popularity_df[popularity_df['tconst'] == tconst][['averageRating', 'numVotes']].values
    if len(movie_rating) > 0:
        movie_rating = {
            "averageRating": movie_rating[0][0],  # Extract the average rating
            "numVotes": movie_rating[0][1]  # Extract the number of votes
        }
    else:
        movie_rating = {"averageRating": "Unknown", "numVotes": "Unknown"}  # Default values if no data found

    # Combine and return the results in a dictionary
    return {
        "Title": movie_name,
        "Actors": movie_actors,
        "Directors": movie_directors,
        "Genres": movie_genres,
        "Rating": movie_rating
    }


def watch_list(watchedMovie, watchedMoviesIds):
    # Filter the genres DataFrame for movies matching the given name
    matching_movies = genres_df[genres_df['primaryTitle'] == watchedMovie]

    if matching_movies.empty:
        print(f"No movie found with the name '{watchedMovie}'.")
        return

    if len(matching_movies) > 1:
        print(f"Multiple movies found with the name '{watchedMovie}':")
        for idx, row in matching_movies.iterrows():
            # Get movie details using get_movie_details
            movie_details = get_movie_details(row['tconst'])
            print(f"[{idx}] {row['primaryTitle']} ({row['titleType']}, Genres: {row['genres']})")
            print("  Details:")
            print(f"    Actors: {', '.join(movie_details['Actors']) if movie_details['Actors'] else 'Unknown'}")
            print(f"    Directors: {', '.join(movie_details['Directors']) if movie_details['Directors'] else 'Unknown'}")
            print(f"    Genres: {movie_details['Genres']}")
            print(f"    Rating: {movie_details['Rating']['averageRating']} (Votes: {movie_details['Rating']['numVotes']})")

        try:
            selected_idx = int(input("Enter the number corresponding to the correct movie: "))
            selected_movie = matching_movies.loc[selected_idx]
        except (ValueError, KeyError):
            print("Invalid selection. No movie added to the watch list.")
            return
    else:
        # If there's only one match, select it automatically
        selected_movie = matching_movies.iloc[0]

    # Add the selected movie's ID to the watched list
    watchedMoviesIds.append(selected_movie['tconst'])
    print(f"Added '{selected_movie['primaryTitle']}' (ID: {selected_movie['tconst']}) to the watch list.")


def recommend_movies(movie_ids, top_n=10):
    """Recommend movies similar to the given list of movie IDs along with unique similarity scores."""
    # Ensure input is a list
    if isinstance(movie_ids, str):
        movie_ids = [movie_ids]
    
    # Get indices of all valid movie IDs
    movie_indices = combined_df.index[combined_df['tconst'].isin(movie_ids)].tolist()
    if not movie_indices:
        return "No valid movie IDs found."
    
    # Compute combined similarity scores
    similarity = cosine_similarity(feature_matrix[movie_indices], feature_matrix)
    combined_similarity = similarity.mean(axis=0)  # Average similarity across all input movies
    
    # Get the indices of the top N most similar movies (excluding the input movies)
    similar_indices = combined_similarity.argsort()[::-1]  # Sort by similarity scores in descending order
    similarity_scores = combined_similarity[similar_indices]  # Extract corresponding similarity scores
    
    # Get the recommended movies with similarity scores
    recommended_movies = combined_df.iloc[similar_indices]
    recommended_movies = recommended_movies.copy()
    recommended_movies['similarity_score'] = similarity_scores  # Add similarity scores to the output

    # Ensure unique tconst values
    recommended_movies = recommended_movies.drop_duplicates(subset='tconst', keep='first')

    # Exclude the input movies and limit to top N results
    recommended_movies = recommended_movies[~recommended_movies['tconst'].isin(movie_ids)].head(top_n)

    return recommended_movies[['tconst', 'similarity_score']]

def printDetails(movie, id):
    if id == "id":
        matching_movies = genres_df[genres_df['tconst'] == movie]
    elif id == "name":
        matching_movies = genres_df[genres_df['primaryTitle'] == movie]
    for idx, row in matching_movies.iterrows():
        movie_details = get_movie_details(row['tconst'])
        print(f"[{idx}] {row['primaryTitle']} ({row['titleType']}, Genres: {row['genres']})")
        print("  Details:")
        print(f"    Actors: {', '.join(movie_details['Actors']) if movie_details['Actors'] else 'Unknown'}")
        print(f"    Directors: {', '.join(movie_details['Directors']) if movie_details['Directors'] else 'Unknown'}")
        print(f"    Genres: {movie_details['Genres']}")
        print(f"    Rating: {movie_details['Rating']['averageRating']} (Votes: {movie_details['Rating']['numVotes']})")

watchedMoviesIds = []


def main():
    x = 1
    print('''
Welcome to the movie recommendation system
Please choose from the following:
    1- Add to the watched list
    2- Show the watched list
    3- Get details for a movie
    4- Recommend a movie based on your watched list
    5- Recommend a movie based on a single movie
    6- End the program
''')
    while x != 0:
        choice = input("Please Enter Your Choice: ")

        if choice == "1":
            movie = input("Enter The Movie Name: ")
            watch_list(movie, watchedMoviesIds)

        elif choice == "2":
            for movie in watchedMoviesIds:
                printDetails(movie, "id")

        elif choice == "3":
            movie = input("Enter The Movie Name: ")
            printDetails(movie, "name")

        elif choice == "4":
            rec = recommend_movies(watchedMoviesIds)
            for _, movie in rec.iterrows():
                details = get_movie_details(movie['tconst'])
                print("Title: ", details["Title"],  ", Genres: ", details["Genres"], ", Similarity: ", movie['similarity_score'])

        elif choice == "5":
            movie = input("Enter The Movie Name: ")
            rec = recommend_movies(movie)
            details = get_movie_details(movie['tconst'])
            print("Title: ", details["Title"],  ", Genres: ", details["Genres"], ", Similarity", rec['similarity_score'])

        elif choice == "6":
            x = 0

        else: 
            print("invalid input")

main()