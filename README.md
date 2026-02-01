# Local-First Agentic Job Searcher

A modular, privacy-focused job scraping system that runs locally. It uses **Playwright** for stealthy browsing and a **Local LLM** (via LM Studio) to analyze job postings and compile them into an Excel spreadsheet.

## Features
*   **Stealth Navigation**: Uses Playwright with human-like delays, scrolling, and random intervals to avoid bot detection.
*   **Local AI Processing**: Connects to LM Studio (`localhost:1234`) to extract structured data (Company, Position, Description, Date) without sending data to the cloud.
*   **Smart extraction**: Cleans HTML to save tokens before sending to the LLM.
*   **Excel Output**: Generates a formatted `jobs_found.xlsx` file with text wrapping.

## Prerequisites
1.  **Python 3.10+** installed.
2.  **LM Studio** installed and running.
    *   Load a model (e.g., Mistral, Llama 3, Phi-3).
    *   Start the **Local Server** on strict port `1234`.

## Installation

1.  Clone this repository or download the files.
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install Playwright browsers:
    ```bash
    playwright install
    ```

## Configuration
Edit `config.py` to customize your search:
*   `JOB_ROLES`: List of job titles to search for.
*   `LOCATION`: Target city/region.
*   `SITES`: Enable/Disable Seek or LinkedIn.
*   `HEADLESS_MODE`: Set to `True` to hide the browser, `False` to watch it work (default).

## Usage

Run the main script:
```bash
python main.py
```

The bot will:
1.  Open a browser window.
2.  Navigate to the selected job boards.
3.  Search for your defined roles.
4.  Scrape job details and use the LLM to structure the data.
5.  Save the results to `jobs_found.xlsx`.

### Generate Cover Letter
To generate a tailored cover letter for the first job in your list:
1.  Ensure `Khun Okkar - CV.pdf` and `Khun Okkar - Cover Letter Format.docx` are in the project folder.
2.  Run:
    ```bash
    python generate_cover_letter.py
    ```
3.  The script will output a new `.docx` file (e.g., `Cover_Letter_Company_Position.docx`).

## Project Structure
*   `main.py`: The orchestrator that manages the workflow.
*   `browser_agent.py`: Handles Playwright navigation and human emulation.
*   `extractor.py`: Cleans HTML and interfaces with the Local LLM.
*   `config.py`: Central configuration file.
