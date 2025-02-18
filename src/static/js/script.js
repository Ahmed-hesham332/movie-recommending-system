document.addEventListener("DOMContentLoaded", () => {
  const movieInput = document.getElementById("movieInput");
  const searchButton = document.getElementById("searchButton");
  const recommendationsContainer = document.getElementById("recommendationsContainer");

  searchButton.addEventListener("click", async () => {
    const movieName = movieInput.value.trim();
    if (movieName) {
      try {
        const response = await fetch(`http://127.0.0.1:80/recommend?movie_name=${encodeURIComponent(movieName)}`);
        const data = await response.json();
        
        if (data.error) {
          recommendationsContainer.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
          displayRecommendations(data);
        }
      } catch (error) {
        recommendationsContainer.innerHTML = `<p class="error">Error fetching recommendations.</p>`;
      }
    }
  });

  function displayRecommendations(recommendations) {
    recommendationsContainer.innerHTML = "";
    recommendations.forEach((movie) => {
      const movieCard = document.createElement("div");
      movieCard.className = "movie-card";
      movieCard.innerHTML = `
        <div class="movie-title">${movie.title}</div>

        <div class="movie-info">
        Release Year: ${movie.release_year}<br>
        Genre: ${movie.genres}<br>
        <br>
        Overview: ${movie.overview}
        </div>
      `;
      recommendationsContainer.appendChild(movieCard);
    });
  }
});
