import pandas as pd
import numpy as np

# Loading the datasets
cols_req = ['title', 'year', 'director', 'runtime', 'genre', 'imdbRating', 'imdbVotes', 'cast']
df = pd.read_csv('movies_initial.csv', usecols=cols_req)
box_office = pd.read_csv('box_office.csv')

# Data Cleaning - Movies Dataset

df.dropna(subset=['imdbRating', 'runtime', 'genre', 'imdbVotes'], inplace=True)

df['runtime'] = df['runtime'].str.replace(' min', '', regex=False)
df = df[df['runtime'].str.isnumeric()]
df['runtime'] = df['runtime'].astype(int)

df['imdbVotes'] = df['imdbVotes'].astype(str).str.replace(',', '', regex=False)
df['imdbVotes'] = pd.to_numeric(df['imdbVotes'], errors='coerce')
df.dropna(subset=['imdbVotes'], inplace=True)
df['imdbVotes'] = df['imdbVotes'].astype(int)

df['imdbRating'] = df['imdbRating'].astype(float)


# Compute Custom Rating (Genuine Rating & Box Office) user k acc kuch bhi rkhlo

max_votes = df['imdbVotes'].max()
df['genuine_rating'] = df['imdbRating'] * (
    1 + 0.5 * np.log10(df['imdbVotes'] + 1) / np.log10(max_votes + 1)
)

df['title_clean'] = df['title'].str.lower().str.strip()
box_office['title_clean'] = box_office['Release Group'].str.lower().str.strip()
df['year'] = pd.to_numeric(df['year'], errors='coerce')
box_office['year'] = pd.to_numeric(box_office['year'], errors='coerce')
box_office['Worldwide'] = box_office['Worldwide'].replace(r'[\$,]', '', regex=True).astype(float)

# Merging box office data
df = pd.merge(df, box_office[['title_clean', 'year', 'Worldwide']], on=['title_clean', 'year'], how='left')
# Add box office score and adjusted rating
df['box_score'] = np.log10(df['Worldwide'] + 1).fillna(0)
df['adjusted_rating'] = 0.7 * df['genuine_rating'] + 0.3 * df['box_score']


# Taking inputs from users (custom)

print("🎬 Welcome to the Movie Recommender!")
director_input = input("Enter director name (or press Enter to skip): ").strip().lower()
actor_input = input("Enter actor/actress name (or press Enter to skip): ").strip().lower()
min_runtime = input("Enter minimum runtime in minutes (or press Enter to skip): ").strip()
min_rating = input("Enter minimum IMDb rating (or press Enter to skip): ").strip()
min_box = input("Enter minimum worldwide box office in USD (or press Enter to skip): ").strip()

filtered = df.copy()

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
    pass

try:
    min_box_val = float(min_box)
    filtered = filtered[filtered['Worldwide'] >= min_box_val]
except ValueError:
    pass

# Showing the Filtered Top Movies

if filtered.empty:
    print("\n❌ No movies found with the given criteria.")
else:
    top = filtered.sort_values(by='adjusted_rating', ascending=False)
    top['Worldwide'] = top['Worldwide'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")

    pd.set_option('display.float_format', '{:.2f}'.format)

    print("\n🎬 Top Movies Based on Your Filters:\n")
    print(top[['title', 'year', 'director', 'runtime', 'imdbRating', 'Worldwide', 'adjusted_rating']].head(6).to_string(
        index=False))

# Extra Insights

# Director statistics
director_stats = df.groupby('director').agg(
    avg_rating=('imdbRating', 'mean'),
    avg_runtime=('runtime', 'mean'),
    movie_count=('title', 'count')
).sort_values(by='avg_rating', ascending=False)

print("\n🎬 Top Directors by Avg IMDb Rating:")
print(director_stats.head())

# Genre statistics
df['genre'] = df['genre'].str.split(', ')
genre_exploded = df.explode('genre')

genre_stats = genre_exploded.groupby('genre').agg(
    avg_rating=('imdbRating', 'mean'),
    avg_runtime=('runtime', 'mean'),
    movie_count=('title', 'count')
).sort_values(by='avg_rating', ascending=False)

print("\n📚 Top Genres by Avg IMDb Rating:")
print(genre_stats.head(10))

# Pivot table - Year × Genre
pivot_table = pd.pivot_table(
    genre_exploded,
    values='imdbRating',
    index='year',
    columns='genre',
    aggfunc='mean'
)

print("\n📊 IMDb Rating by Year and Genre (Recent Years):")
print(pivot_table.tail(5))

worldwide_year_total = df.pivot_table(
    values='Worldwide',
    index='year',
    aggfunc='sum'
)

print("\n💰 Total Worldwide Box Office Collection by Year:")
print(worldwide_year_total.tail(10))
