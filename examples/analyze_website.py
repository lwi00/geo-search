"""
Example script demonstrating how to use GeoSearch to analyze a website.
"""
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import GeoSearch

def analyze_website(url: str):
    """
    Analyze a website and save the results.
    
    Args:
        url (str): The URL to analyze
    """
    # Initialize GeoSearch
    geo_search = GeoSearch()
    
    # Create output directory if it doesn't exist
    output_dir = "analysis_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename based on URL and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").replace("/", "_").strip("_")
    output_file = os.path.join(output_dir, f"{domain}_{timestamp}.json")
    
    try:
        # Run the analysis
        results = geo_search.analyze_url(url, output_file)
        print("\n✅ Analysis completed successfully!")
        print(f"📁 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error analyzing {url}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_website.py <url>")
        print("Example: python analyze_website.py https://example.com")
        sys.exit(1)
        
    url = sys.argv[1]
    analyze_website(url) 