"""
Script to download required NLTK data.
"""
import nltk

def download_nltk_data():
    """Download required NLTK data packages."""
    required_packages = [
        'punkt',  # For sentence tokenization
        'averaged_perceptron_tagger',  # For part-of-speech tagging
        'wordnet',  # For word meanings and synonyms
        'stopwords'  # For stop words
    ]
    
    for package in required_packages:
        print(f"Downloading {package}...")
        nltk.download(package, quiet=True)
        print(f"✓ {package} downloaded successfully")

if __name__ == "__main__":
    download_nltk_data() 