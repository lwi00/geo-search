"""
Main script for GeoSearch - SEO and Gemini Analysis Tool
"""
import os
import json
import argparse
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv
from scraper.scraper import WebScraper
from seo.seo_analyzer import SEOAnalyzer
from seo.seo_metrics import SEOMetrics

class GeoSearch:
    def __init__(self):
        """Initialize GeoSearch with its components."""
        self.scraper = WebScraper()
        self.seo_analyzer = SEOAnalyzer()
        self.seo_metrics = SEOMetrics()
        
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
        
        # Compute advanced metrics
        print("📈 Computing advanced metrics...")
        advanced_metrics = self.seo_metrics.compute_metrics(seo_results)
        
        # Prepare final results
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'seo_analysis': seo_results,
            'advanced_metrics': advanced_metrics,
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
        metrics = results['advanced_metrics']
        
        # Prepare sections
        meta = seo['meta_tags']
        content = seo['content_analysis']
        links = seo['link_analysis']
        images = seo['image_analysis']
        technical = seo['technical_seo']
        
        summary = [
            "\n📊 SEO Analysis Summary",
            "=" * 50,
            
            f"\n🏆 Overall Score: {metrics['overall_score']}/100",
            
            "\n📑 Meta Information:",
            f"• Title: {meta['title']['content']} ({meta['title']['length']} chars) - Score: {metrics['technical_score']['title']['score']}/100",
            f"• Meta Description: {meta['meta_description']['content'][:100]}..." if meta['meta_description']['content'] else "• Meta Description: Missing",
            f"• Meta Description Score: {metrics['technical_score']['meta_description']['score']}/100",
            f"• Robots Directive: {meta['robots'] or 'Not specified'}",
            
            "\n📝 Content Analysis:",
            f"• Content Quality Score: {metrics['content_quality']['text_html_ratio']['score']}/100",
            f"• Total Words: {seo['keyword_analysis']['total_words']}",
            f"• Unique Words: {seo['keyword_analysis']['unique_words']}",
            f"• Paragraphs: {content['paragraph_count']}",
            f"• Text/HTML Ratio: {content['text_html_ratio']:.2f}%",
            f"• Readability Score: {metrics['readability']['paragraph_length']['score']}/100",
            
            "\n🔗 Link Analysis:",
            f"• Internal Links: {links['internal_links']['count']} (Score: {metrics['link_quality']['internal_links']['score']}/100)",
            f"• External Links: {links['external_links']['count']} (Score: {metrics['link_quality']['external_links']['score']}/100)",
            
            "\n🖼️ Image Analysis:",
            f"• Total Images: {images['total_images']}",
            f"• Images with Alt Text: {images['images_with_alt']} (Score: {metrics['image_optimization']['alt_text']['score']}/100)",
            f"• Images with Dimensions: {images['images_with_dimensions']}",
            
            "\n⚙️ Technical SEO:",
            f"• Technical Score: {metrics['technical_score']['technical_score']}/100",
            f"• Viewport Meta: {'✅' if technical['has_viewport'] else '❌'}",
            f"• Favicon: {'✅' if technical['has_favicon'] else '❌'}",
            f"• Structured Data: {'✅' if technical['has_structured_data'] else '❌'}",
            f"• Analytics: {'✅' if technical['has_analytics'] else '❌'}",
            
            "\n🔑 Top Keywords:",
        ]
        
        # Add top 5 keywords with their scores
        for word, data in list(metrics['keyword_optimization']['keyword_usage'].items())[:5]:
            summary.append(f"• {word}: {data['density']:.2f}% density (Score: {data['score']}/100)")
            if data['in_title']:
                summary[-1] += " [in title]"
            if data['in_meta_description']:
                summary[-1] += " [in meta]"
        
        # Add recommendations
        if metrics['recommendations']:
            summary.extend([
                "\n📋 Recommendations:",
                "=" * 50
            ])
            for rec in metrics['recommendations']:
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                summary.append(f"{priority_emoji} {rec['message']}")
            
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