# GeoSearch

A tool for analyzing websites using Google's Gemini AI and comparing the results with traditional SEO metrics.

## Project Structure

```
geo-search/
├── src/
│   ├── __init__.py
│   └── scraper.py
├── tests/
├── .env.template
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows (PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
```
- Windows (Command Prompt):
```cmd
.\venv\Scripts\activate.bat
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
- Copy `.env.template` to `.env`
- Add your Gemini API key

## Features

### Current Implementation
- Basic web scraping functionality
  - Page content extraction
  - Meta tags analysis
  - Header structure analysis

### Planned Features
- Gemini AI analysis
- Traditional SEO metrics
- Comparison framework
- Results visualization

## Usage

[Coming soon]

## Contributing

[Coming soon]

## License

[Coming soon]