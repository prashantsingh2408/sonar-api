# Perplexity API Project Setup Guide

This guide will help you set up and run the Perplexity API project in your local environment.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)
- A Perplexity API key (get it from https://www.perplexity.ai/settings/api)

## Project Structure

```
sonar-api/
├── venv/                  # Virtual environment directory
├── env_file              # Environment variables file (not in git)
├── env_file.example      # Example environment file (safe to commit)
├── perplexity_api.py     # Main API script with interactive menu
├── CURL-TESTING.md       # API test cases and examples
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README-SETUP.md      # This setup guide
```

## Setup Instructions

### 1. Clone the Repository (if using Git)
```bash
git clone <repository-url>
cd sonar-api
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt when the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

1. Copy the example environment file:
```bash
cp env_file.example env_file
```

2. Edit `env_file` and replace the placeholder with your actual API key:
```bash
PERPLEXITY_API_KEY=your_actual_api_key_here
```

## Running the Project

1. Ensure your virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
# or
# .\venv\Scripts\activate  # Windows
```

2. Run the interactive script:
```bash
python perplexity_api.py
```

The script provides an interactive menu with the following options:
1. Test a model
2. Show available models
3. Verify web search capability
4. Exit

## Available Models

### Search Models
- sonar (128k context) - Lightweight search model
- sonar-pro (200k context) - Advanced search model

### Reasoning Models
- sonar-reasoning (128k context) - Fast reasoning model
- sonar-reasoning-pro (128k context) - Premier reasoning model

### Research Models
- sonar-deep-research (128k context) - Expert research model

### Offline Models
- r1-1776 (128k context) - Offline chat model

## Usage Examples

### Using the Interactive Menu
1. Select option 1 to test a model
2. Choose a model from the menu
3. Enter your prompt
4. Optionally configure advanced settings:
   - System prompt
   - Temperature
   - Max tokens
   - Streaming
   - Web search verification

### Using the API in Your Code
```python
from perplexity_api import PerplexityAPI

# Initialize the API
api = PerplexityAPI()

# Basic usage
result = api.call_api(
    prompt="Your prompt here",
    model="sonar"  # or any other available model
)

# Advanced usage with parameters
result = api.call_api(
    prompt="Your prompt here",
    model="sonar-pro",
    system_prompt="Custom system prompt",
    temperature=0.7,
    max_tokens=1000,
    stream=True,
    verify_web=True
)
```

## Troubleshooting

1. **ModuleNotFoundError**: If you see this error, ensure:
   - Virtual environment is activated
   - Dependencies are installed (`pip install -r requirements.txt`)

2. **API Key Error**: If you see "PERPLEXITY_API_KEY not found in environment variables":
   - Check if `env_file` exists
   - Verify the API key is correctly set in `env_file`
   - Ensure you're running the script from the correct directory

3. **400 Bad Request Error**: If you encounter API errors:
   - Verify you're using a valid model name
   - Check the model's capabilities (web search, context length)
   - Review the error message for specific details
   - Consult CURL-TESTING.md for example requests

4. **Permission Issues**: If you encounter permission errors:
   - Ensure you have execute permissions for the virtual environment
   - Try recreating the virtual environment

## Security Notes

- Never commit your actual `env_file` to version control
- Keep your API key secure
- Use `env_file.example` as a template
- The `.gitignore` file is configured to exclude sensitive files

## Additional Resources

- For detailed API documentation: https://docs.perplexity.ai/
- For model information: https://docs.perplexity.ai/models/model-cards
- For API test cases: See CURL-TESTING.md

## Deactivating Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```
