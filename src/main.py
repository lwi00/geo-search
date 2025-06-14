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
from .seo_metrics import SEOMetrics
from .ai_readability import AIReadabilityAnalyzer
from .crawlability import CrawlabilityAnalyzer
from .readability import ReadabilityAnalyzer

class GeoSearch:
    def __init__(self):
        """Initialize GeoSearch with its components."""
        self.scraper = WebScraper()
        self.seo_analyzer = SEOAnalyzer()
        self.metrics = SEOMetrics()
        self.ai_readability = AIReadabilityAnalyzer()
        self.crawlability = CrawlabilityAnalyzer()
        self.readability = ReadabilityAnalyzer()
        
        # Load environment variables
        load_dotenv()
        
    def analyze_url(self, url: str, output_file: Optional[str] = None) -> Dict:
        """
        Analyze a URL for SEO, AI readability, and crawlability.
        
        Args:
            url (str): URL to analyze
            output_file (Optional[str]): Path to save the analysis results
            
        Returns:
            dict: Analysis results
        """
        print(f"\n🔍 Analyzing URL: {url}")
        
        # Fetch the page
        print("📥 Fetching page content...")
        html_content = self.scraper.fetch_page(url)
        if not html_content:
            return {"error": f"Failed to fetch content from {url}"}
            
        # Perform SEO analysis
        print("📊 Performing SEO analysis...")
        seo_results = self.seo_analyzer.analyze(html_content, url)
        
        # Compute advanced metrics
        print("📈 Computing advanced metrics...")
        metrics_results = self.metrics.compute_metrics(seo_results)
        
        # Perform AI readability analysis
        ai_readability = self.analyze_ai_readability(html_content, seo_results)
        
        # Perform crawlability analysis
        crawlability_analysis = self.crawlability.analyze_crawlability(url, html_content)
        
        # Perform text readability analysis
        readability_analysis = self.readability.analyze_readability(html_content)
        
        # Combine results
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'seo_analysis': seo_results,
            'advanced_metrics': metrics_results,
            'ai_readability': ai_readability,
            'crawlability': crawlability_analysis,
            'readability': readability_analysis
        }
        
        # Save results if output file is specified
        if output_file:
            self._save_results(results, output_file)
            print(f"💾 Results saved to: {output_file}")
            
        return results
    
    def analyze_ai_readability(self, content: str, seo_analysis: Dict) -> Dict:
        """
        Analyze AI readability metrics.
        
        Args:
            content (str): Raw HTML content
            seo_analysis (dict): Output from SEOAnalyzer
            
        Returns:
            dict: AI readability analysis results
        """
        # Analyze SEO structure
        seo_structure = self.ai_readability.analyze_seo_structure(seo_analysis)

        # Analyze semantic and structure
        semantic_structure = self.ai_readability.analyze_semantic_and_structure(content, seo_analysis)

        return {
            "seo_structure": seo_structure,
            "semantic_structure": semantic_structure
        }
    
    def _save_results(self, results: Dict, output_file: str):
        """Save analysis results to a JSON file."""
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
    def _format_seo_summary(self, results: Dict) -> str:
        """Format SEO analysis results for console output."""
        seo = results['seo_analysis']
        metrics = results['advanced_metrics']
        ai = results['ai_readability']
        crawl = results['crawlability']
        readability = results['readability']
        
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
            f"• Meta Description: {meta['meta_description']['content'][:100]}...",
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
            
        # Add advanced metrics
        summary.extend([
            "\n📈 Advanced Metrics",
            "=" * 50,
            
            "\n📊 Content Quality:",
            f"• Content Length Score: {metrics['content_quality']['content_length_score']:.2%}",
            f"• Heading Structure Score: {metrics['content_quality']['heading_structure_score']:.2%}",
            f"• Paragraph Structure Score: {metrics['content_quality']['paragraph_structure_score']:.2%}",
            f"• Overall Content Score: {metrics['content_quality']['overall_content_score']:.2%}",
            
            "\n📚 Readability:",
            f"• Flesch Reading Ease: {metrics['readability']['flesch_reading_ease']:.1f}",
            f"• Readability Level: {metrics['readability']['readability_level']}",
            f"• Average Sentence Length: {metrics['readability']['avg_sentence_length']:.1f} words",
            
            "\n🔍 Keyword Optimization:",
            f"• Keyword Optimization Score: {metrics['keyword_optimization']['keyword_optimization_score']:.2%}",
            
            "\n🔗 Link Quality:",
            f"• Internal/External Ratio: {metrics['link_quality']['internal_external_ratio']:.2%}",
            f"• Link Text Quality Score: {metrics['link_quality']['overall_link_quality_score']:.2%}",
            
            "\n🖼️ Image Optimization:",
            f"• Alt Text Score: {metrics['image_optimization']['alt_text_score']:.2%}",
            f"• Dimensions Score: {metrics['image_optimization']['dimensions_score']:.2%}",
            f"• Overall Image Score: {metrics['image_optimization']['overall_image_score']:.2%}",
            
            "\n📊 Overall Scores:",
            f"• Technical Score: {metrics['technical_score']['overall_technical_score']:.2%}",
            f"• Overall SEO Score: {metrics['overall_score']['overall_score']:.2%}",
        ])
            
        # Add AI readability summary
        summary.extend([
            "\n🤖 AI Readability:",
            f"SEO Structure: {ai['seo_structure']['title_tag_length']['explanation']}",
            f"Semantic Usage: {ai['semantic_structure']['semantic_element_usage']['explanation']}",
            f"HTML Validation: {ai['semantic_structure']['html_validation_errors']['explanation']}",
            f"Heading Hierarchy: {ai['semantic_structure']['heading_hierarchy_order']['explanation']}"
        ])
            
        # Add crawlability summary
        summary.extend([
            "\n🕷️ Crawlability:",
            f"Indexability: {crawl['indexability']['explanation']}",
            f"Sitemap Status: {crawl['sitemap_status']['explanation']}",
            f"Text-to-HTML Ratio: {crawl['text_ratio']['explanation']}",
            f"Page Load Time: {crawl['load_time']['explanation']}",
            f"Overall Crawlability: {crawl['overall_score']['explanation']}"
        ])
            
        # Add text readability summary
        summary.extend([
            "\n📚 Text Readability:",
            f"Flesch Reading Ease: {readability['flesch_reading_ease']['explanation']}",
            f"Sentence Length: {readability['average_sentence_length']['explanation']}",
            f"Lexical Complexity: {readability['lexical_complexity']['explanation']}",
            f"Overall Readability: {readability['overall_score']['explanation']}"
        ])
            
        # Add LLM bot analysis section
        if crawl['llm_bot_analysis']['robots_txt_exists']:
            summary.extend([
                "\n🤖 LLM Bot Analysis:",
                f"Robots.txt: {crawl['llm_bot_analysis']['robots_txt_url']}",
                f"Summary: {crawl['llm_bot_analysis']['summary']}"
            ])
            
            # Add detailed bot directives
            for bot_name, directive in crawl['llm_bot_analysis']['bot_directives'].items():
                if directive['user_agents_found']:
                    summary.append(f"\n{bot_name} ({directive['company']}):")
                    summary.append(f"• {directive['explanation']}")
                    if directive['crawl_delay']:
                        summary.append(f"• Crawl delay: {directive['crawl_delay']}s")
                    if directive['disallowed_paths']:
                        summary.append(f"• Blocked paths: {', '.join(directive['disallowed_paths'])}")

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