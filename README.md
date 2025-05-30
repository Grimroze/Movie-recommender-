# 🎬 Movie Recommender 

A Python-based command-line movie recommender system that filters and ranks movies based on user preferences like director, actor, runtime, and IMDb rating. It also computes a custom "genuine rating" that balances rating quality with popularity to recommend more reliable films.

---

## 🚀 Features

- Filter movies by:
  - 🎥 Director
  - 🎭 Actor/Actress
  - ⏱️ Minimum Runtime
  - ⭐ Minimum IMDb Rating
- Calculates a **"genuine rating"** that blends IMDb rating with vote count using a weighted scoring model
- Sorts results by quality, popularity, and credibility
- Outputs a ranked list of top 10 matching movies
- Handles messy data (runtime, votes, etc.) gracefully

---

## 📊 Scoring Formula

By default, the recommender uses a weighted IMDb-style formula to compute a more trustworthy score:
@grimroze
