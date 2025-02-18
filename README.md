# Movie Recommendation System

![Movie Recommendation System](https://img.shields.io/badge/status-active-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.9%2B-blue) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.85%2B-green) 
![Docker](https://img.shields.io/badge/Docker-20.10%2B-orange)

A Movie Recommendation System built with **FastAPI** and **Docker** that provides personalized movie recommendations based on user input. The system uses a dataset of movies and recommends similar movies based on genres, release year, and overview.
The dataset containts 1M movies but after the preprossing, i used around 400k movie.

---

## Features

- **Search for Movies**: Enter a movie name to get recommendations.
- **Dynamic Recommendations**: Displays recommended movies with details like title, release year, genres, and overview.
- **Responsive UI**: Clean and user-friendly interface.
- **Dockerized**: Easy to deploy and run using Docker.

---

## Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas, NumPy, skit-learn, bert model
- **Containerization**: Docker
- **Testing**: Postman

---

## Prerequisites

Before running the project, ensure you have the following apps installed and have the following files:

- **Python 3.9+**
- **Docker** (optional, for containerized deployment)
- **Git** (for cloning the repository)
- **Dataset** (tmdb movies dataset)
- **embedded features** (embed the features using dataEmbedding.py on the refined dataset)
---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed-hesham332/movie_recommendation_system.git
cd movie_recommendation_system
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Running the Project

```bash
uvicorn src.movies:app --host 0.0.0.0 --port 80
```
### Option 2: Run with Docker

```bash
docker build -t movie-recommendation-system .
docker run -p 80:80 movie-recommendation-system
```

## Project Structure

```plaintext
movie_recommendation_system/
├── src/
│   ├── mycache_/           # Cached data
│   ├── dataset/            # Movie dataset
│   ├── embeddedData/       # Embedded data for recommendations
│   ├── templates/          # HTML templates
│   ├── css/                # CSS files
│   ├── js/                 # JavaScript files
│   ├── dataEmbedding.py    # Script for embedding data
│   ├── movies.py           # Movie data processing
│   ├── recommender.py      # Recommendation logic
│   ├── refinedData.py      # Data refinement script
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

## API Endpoints

```bash
GET http://localhost:80/recommend?movie_name=movie_name
```

**Example Request:**

```bash
GET http://localhost:80/recommend?movie_name=Inception
```
**Example Output:**

```json
[
  {
    "title": "Inception",
    "release_year": 2010,
    "genres": "Action, Sci-Fi",
    "overview": "A thief who steals corporate secrets..."
  },
  {
    "title": "Interstellar",
    "release_year": 2014,
    "genres": "Adventure, Drama, Sci-Fi",
    "overview": "A team of explorers travel through a wormhole..."
  }
]
```

## Screenshots

### Home page

### recommendations

## Problems andd Futer improvements

- The application relies on  TMDB Movies Dataset and after a couple use of the application, i have notice that some movies (famous movies) are not included in the dataset.
- The search works ONLY if the movie is between 2010 and 2027 and exists in the dataset
- Any type of spelling mistakes are not detected and if the movie name is wrong for example "avenger" is not the same as "The avengers", the first one will results on movie not found and the second one works.
- The used model is not the best model, due to the limited resources i have to use a smaller model so you can expect some funny suggestions
- Only 9 movies will show and cannot be changed (But these movies are the best according to the model)

## Acknowledgments

- **Full TMDB Movies Dataset 2024 (1M Movies) by asaniczka**

## Contact

For questions or feedback, feel free to reach out:

**Ahmed Husham**

**Email: **modihesho@gmail.com
