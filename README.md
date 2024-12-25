# Movie Recommendation System

## Introduction

The Movie Recommendation System delivers personalized movie suggestions tailored to user preferences, including watched movies, favorite genres, actors, and directors. Leveraging IMDb datasets, it efficiently processes millions of entries, helping users discover new movies effortlessly.

## Features

1. **Data Cleaning and Integration**:
   - Combines and preprocesses IMDb datasets, including actors, directors, genres, and ratings.

2. **Personalized Recommendations**:
   - Recommends movies based on a user's watchlist or a single movie, considering factors like genres and popularity.

3. **Watchlist Management**:
   - Allows users to maintain a watchlist and generate recommendations based on it.

4. **Detailed Movie Insights**:
   - Provides in-depth information such as cast, directors, genres, and ratings.

5. **Efficient Computation**:
   - Employs cosine similarity for fast and accurate recommendations on large datasets.

6. **Interactive Interface**:
   - Features a menu-driven command-line interface for easy interaction.

## Technologies Used

- **Programming Language**: Python
- **Key Libraries**: Pandas, NumPy, Scikit-learn, Joblib, TQDM
- **Development Tools**: Jupyter Notebooks for data preparation and analysis

These tools ensure efficient data handling and reliable recommendation performance.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place IMDb datasets in the `data/` folder and execute data preparation scripts in sequence.

5. Start the program:
   ```bash
   python main.py
   ```

## Usage

1. **Start the Program**:
   - Run `main.py` to access the system.

2. **Features**:
   - Add movies to a watchlist.
   - View and manage your watchlist.
   - Get detailed movie information.
   - Generate recommendations based on your watchlist or a single movie.

3. **Example Commands**:
   - Add to watchlist: `1`
   - Get recommendations: `4`

## Challenges and Limitations

During development, various methods were explored:

1. **FAISS (Facebook AI Similarity Search)**:
   - High computational demands limited its use on large datasets.

2. **Batch Training**:
   - Encountered memory issues and accuracy inconsistencies across batches.

3. **Dimensionality Reduction**:
   - While efficient, it slightly reduced recommendation accuracy.

Ultimately, cosine similarity was chosen for its balance of accuracy and efficiency, given computational constraints.

## Main Program Overview

The `main.py` file serves as the core interface, enabling:

- Loading preprocessed data and models.
- Adding movies to a watchlist.
- Generating recommendations based on watchlists or single movies.
- Displaying detailed movie information.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit changes and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

- **Email**: your.email@example.com
- **GitHub**: [Your GitHub Profile]

## Acknowledgements

Thanks to IMDb for datasets and libraries like Scikit-learn, Pandas, and NumPy for their contributions to this project.

