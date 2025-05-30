import pandas as pd
import numpy as np
import math

cols_req = ['title', 'year', 'director', 'runtime', 'genre', 'imdbRating', 'imdbVotes', 'cast']
df = pd.read_csv('movies_initial.csv', usecols=cols_req)
# using only essential values and cleaning them in NaN
df.dropna(subset=['imdbRating', 'runtime', 'genre', 'imdbVotes'], inplace=True)

# Clean 'runtime' column to int value
df['runtime'] = df['runtime'].str.replace(' min', '', regex=False)
df = df[df['runtime'].str.isnumeric()]
df['runtime'] = df['runtime'].astype(int)

# Clean 'imdbVotes' column
df['imdbVotes'] = df['imdbVotes'].astype(str).str.replace(',', '', regex=False)
df['imdbVotes'] = pd.to_numeric(df['imdbVotes'], errors='coerce')
df.dropna(subset=['imdbVotes'], inplace=True)
df['imdbVotes'] = df['imdbVotes'].astype(int)

# Convert rating to float
df['imdbRating'] = df['imdbRating'].astype(float)

# Compute genuine rating
max_votes = df['imdbVotes'].max()
df['genuine_rating'] = df['imdbRating'] * (
    1 + 0.5 * np.log10(df['imdbVotes'] + 1) / np.log10(max_votes + 1)
)


# taking User inputs (baad m bda bhi skte h )
print("🎬 Welcome to the Movie Recommender!")
director_input = input("Enter director name (or press Enter to skip): ").strip().lower()
actor_input = input("Enter actor/actress name (or press Enter to skip): ").strip().lower()
min_runtime = input("Enter minimum runtime in minutes (or press Enter to skip): ").strip()
min_rating = input("Enter minimum IMDb rating (or press Enter to skip): ").strip()

# Applying the user-taken filters
filtered = df.copy()            # og dataset unchanged h
if director_input:
    filtered = filtered[filtered['director'].str.lower().str.contains(director_input, na=False)]

if actor_input:
    filtered = filtered[filtered['cast'].str.lower().str.contains(actor_input, na=False)]

if min_runtime.isdigit():
    filtered = filtered[filtered['runtime'] >= int(min_runtime)]

try:
    min_rating_val = float(min_rating)
    filtered = filtered[filtered['imdbRating'] >= min_rating_val]
except ValueError:
    pass  # Skip rating filter if input is invalid

# Display the results
if filtered.empty:
    print("\n❌ No movies found with the given criteria.")
else:
    top = filtered.sort_values(by=['genuine_rating', 'imdbRating', 'imdbVotes'], ascending=False)   # highest dikhani h

    # Format output
    pd.set_option('display.float_format', '{:.2f}'.format)

    print("\n🎬 Top Movies Based on Your Filters:\n")
    print(top[['title', 'year', 'director', 'runtime', 'imdbRating', 'imdbVotes', 'genuine_rating']].head(15).to_string(index=False))
