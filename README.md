# GeoSearch - Website Analysis Tool

A comprehensive website analysis tool that combines traditional SEO metrics with AI-powered readability analysis and crawlability assessment.

## Features

### 1. SEO Analysis
- Meta tags analysis (title, description, keywords)
- Content structure evaluation
- Heading hierarchy analysis
- Link analysis (internal/external)
- Image optimization check
- Technical SEO assessment

### 2. Advanced SEO Metrics
- Content quality scoring
- Technical SEO scoring
- Keyword optimization
- Link quality assessment
- Image optimization scoring
- Overall SEO score

### 3. AI Readability Analysis
- SEO structure analysis
- Semantic element usage
- HTML validation
- Heading hierarchy order
- Content structure assessment

### 4. Crawlability Analysis
- Indexability check (robots.txt)
- XML sitemap verification
- Text-to-HTML ratio
- Page load time
- LLM bot directives analysis

### 5. Text Readability Analysis
- Flesch Reading Ease score
- Average sentence length
- Lexical complexity
- Overall readability score

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/geo-search.git
cd geo-search
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```bash
python src/download_nltk_data.py
```

5. Create a `.env` file from the template:
```bash
cp .env.template .env
```

6. Add your Google Gemini API key to the `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage
```bash
python -m src.main https://example.com
```

### Save Results to File
```bash
python -m src.main https://example.com --output results.json
```

### Example Script
```bash
python examples/analyze_website.py https://example.com
```

## Output Format

The tool provides a comprehensive analysis including:

1. **SEO Analysis**
   - Meta tags
   - Content structure
   - Link analysis
   - Image optimization

2. **Advanced Metrics**
   - Content quality score
   - Technical score
   - Keyword optimization
   - Link quality
   - Image optimization
   - Overall score

3. **AI Readability**
   - SEO structure
   - Semantic usage
   - HTML validation
   - Heading hierarchy

4. **Crawlability**
   - Indexability status
   - Sitemap status
   - Text-to-HTML ratio
   - Page load time
   - LLM bot directives

5. **Text Readability**
   - Flesch Reading Ease
   - Sentence length
   - Lexical complexity
   - Overall readability

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Project Structure
```
geo-search/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── scraper.py
│   ├── seo_analyzer.py
│   ├── seo_metrics.py
│   ├── ai_readability.py
│   ├── crawlability.py
│   ├── readability.py
│   └── download_nltk_data.py
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
│   ├── test_seo_analyzer.py
│   ├── test_seo_metrics.py
│   ├── test_ai_readability.py
│   ├── test_crawlability.py
│   └── test_readability.py
├── examples/
│   └── analyze_website.py
├── requirements.txt
├── .env.template
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for AI-powered analysis
- NLTK for text analysis
- BeautifulSoup4 for web scraping