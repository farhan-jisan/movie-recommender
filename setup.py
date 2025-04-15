from setuptools import setup, find_packages

#with open("README.md", "r", encoding = "utf-8") as fh:
    #long_description = fh.read()

Author_Name = "Farhan Tasnim Jisan"

setup(
    name = "Movie_recommender",
    version= 0.1,
    author = Author_Name,
    author_email= 'farhantasnim.22@gmail.com',
    description="A content-based movie recommendation system using NLP and cosine similarity.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "nltk",
        "streamlit"
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires= '>=3.6',


)

