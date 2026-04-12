# Content-Based Movie Recommender System

A content-based movie recommendation system that suggests movies similar to a given input movie using cosine similarity on movie metadata.

## Features
- Recommends 5 similar movies based on genres, keywords, cast, and overview
- Built in Python using Jupyter Notebook
- Web interface using Streamlit for easy interaction

## Screenshots
<img width="1920" height="990" alt="image" src="https://github.com/user-attachments/assets/1d6d6438-5a6f-4fa4-a0cc-26c66afe76c3" />
<img width="1920" height="990" alt="image" src="https://github.com/user-attachments/assets/342a4ef5-fdef-4111-92a3-13699b7fa640" />


## Dataset
This project uses the **TMDB 5000 Movies and Credits datasets**   
Due to licensing restrictions, the datasets are not included in this repository.

## Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Streamlit
- Jupyter Notebook

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download the TMDB datasets and place them in the project directory
4. Run the Streamlit app: `streamlit run app.py`

## Usage

- Open the Jupyter notebook `recommender.ipynb` for the original implementation
- Run `streamlit run app.py` to launch the web interface
