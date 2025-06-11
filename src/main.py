"""
Main script for GeoSearch - SEO and Gemini Analysis Tool
"""
import os
import json
import argparse
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv
from .scraper import WebScraper
from .seo_analyzer import SEOAnalyzer

class GeoSearch:
    def __init__(self):
        """Initialize GeoSearch with its components."""
        self.scraper = WebScraper()
        self.seo_analyzer = SEOAnalyzer()
        
        # Load environment variables
        load_dotenv()
        
    def analyze_url(self, url: str, output_file: Optional[str] = None) -> Dict:
        """
        Analyze a URL using both SEO analysis and Gemini (to be implemented).
        
        Args:
            url (str): The URL to analyze
            output_file (Optional[str]): Path to save the analysis results
            
        Returns:
            Dict: Analysis results
        """
        print(f"\n🔍 Analyzing URL: {url}")
        
        # Fetch the page
        print("📥 Fetching page content...")
        html_content = self.scraper.fetch_page(url)
        if not html_content:
            raise Exception(f"Failed to fetch content from {url}")
            
        # Perform SEO analysis
        print("📊 Performing SEO analysis...")
        seo_results = self.seo_analyzer.analyze(html_content, url)
        
        # Prepare final results
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'seo_analysis': seo_results,
            # Gemini analysis will be added here
        }
        
        # Save results if output file is specified
        if output_file:
            self._save_results(results, output_file)
            print(f"💾 Results saved to: {output_file}")
            
        return results
    
    def _save_results(self, results: Dict, output_file: str):
        """Save analysis results to a JSON file."""
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
    def _format_seo_summary(self, results: Dict) -> str:
        """Format SEO analysis results for console output."""
        seo = results['seo_analysis']
        
        # Prepare sections
        meta = seo['meta_tags']
        content = seo['content_analysis']
        links = seo['link_analysis']
        images = seo['image_analysis']
        technical = seo['technical_seo']
        
        summary = [
            "\n📊 SEO Analysis Summary",
            "=" * 50,
            
            "\n📑 Meta Information:",
            f"• Title: {meta['title']['content']} ({meta['title']['length']} chars)",
            f"• Meta Description: {meta['meta_description']['content'][:100]}..." if meta['meta_description']['content'] else "• Meta Description: Missing",
            f"• Robots Directive: {meta['robots'] or 'Not specified'}",
            
            "\n📝 Content Analysis:",
            f"• Total Words: {seo['keyword_analysis']['total_words']}",
            f"• Unique Words: {seo['keyword_analysis']['unique_words']}",
            f"• Paragraphs: {content['paragraph_count']}",
            f"• Text/HTML Ratio: {content['text_html_ratio']:.2f}%",
            
            "\n🔗 Link Analysis:",
            f"• Internal Links: {links['internal_links']['count']}",
            f"• External Links: {links['external_links']['count']}",
            
            "\n🖼️ Image Analysis:",
            f"• Total Images: {images['total_images']}",
            f"• Images with Alt Text: {images['images_with_alt']}",
            f"• Images with Dimensions: {images['images_with_dimensions']}",
            
            "\n⚙️ Technical SEO:",
            f"• Viewport Meta: {'✅' if technical['has_viewport'] else '❌'}",
            f"• Favicon: {'✅' if technical['has_favicon'] else '❌'}",
            f"• Structured Data: {'✅' if technical['has_structured_data'] else '❌'}",
            f"• Analytics: {'✅' if technical['has_analytics'] else '❌'}",
            
            "\n🔑 Top Keywords:",
        ]
        
        # Add top 5 keywords
        for word, data in list(seo['keyword_analysis']['top_keywords'].items())[:5]:
            summary.append(f"• {word}: {data['count']} times ({data['density']:.2f}%)")
            
        return "\n".join(summary)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="GeoSearch - Analyze websites using SEO metrics and Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'url',
        help="URL to analyze"
    )
    
    parser.add_argument(
        '-o', '--output',
        help="Output JSON file path",
        default=None
    )
    
    parser.add_argument(
        '--no-summary',
        help="Don't display the summary in console",
        action='store_true'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize and run analysis
        geo_search = GeoSearch()
        results = geo_search.analyze_url(args.url, args.output)
        
        # Display summary unless --no-summary is specified
        if not args.no_summary:
            print(geo_search._format_seo_summary(results))
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 