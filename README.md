# Resume Extraction System

An LLM-powered Python pipeline that reads resume text files, extracts key candidate information into a structured schema, and saves both raw and parsed outputs for downstream analysis.

This project is useful for learning how to combine:

- configurable data pipelines,
- OpenAI structured outputs,
- Pydantic response schemas, and
- Excel export for recruiter-friendly review.

## Features

- Processes multiple resumes from a folder in one run
- Supports structured extraction with the OpenAI API
- Validates extracted fields with a Pydantic schema
- Saves raw API responses as JSON
- Saves parsed candidate data as JSON
- Exports consolidated results to Excel
- Writes run logs with summary metrics
- Includes retry handling for transient API failures

## What It Extracts

For each resume, the pipeline extracts:

- candidate name
- email
- phone number
- current location
- total experience
- relevant experience
- current or latest job title
- current or latest company
- highest education
- notice period

It also stores a short reasoning field for each extracted value.

## Current Input Format

This version currently supports only plain text resume files:

- `.txt` resumes are supported
- `.pdf` and `.docx` resumes are not processed in the current implementation

## Project Structure

```text
Resume-Extraction-System/
|-- config/
|   |-- config.yaml
|-- data/
|   |-- new_resumes/
|   `-- resumes/
|-- src/
|   |-- config_loader.py
|   |-- data_loader.py
|   |-- data_saver.py
|   |-- llm_client.py
|   |-- models.py
|   |-- processor.py
|   |-- prompt_builder.py
|   `-- retry_handler.py
|-- main.py
|-- requirements.txt
`-- README.md
```

## How It Works

1. Loads settings from `config/config.yaml`
2. Loads the OpenAI API key from the `.env` file
3. Reads all `.txt` resumes from the configured input folder
4. Builds a prompt for each resume
5. Sends the prompt to the OpenAI model using structured parsing
6. Saves:
   - raw API output as JSON
   - parsed candidate output as JSON
   - combined results as Excel
   - logs for the run

## Tech Stack

- Python
- OpenAI Python SDK
- Pydantic
- Pandas
- PyYAML
- python-dotenv

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- an OpenAI API key
- resume files in `.txt` format

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Resume-Extraction-System
```

### 2. Create and activate a virtual environment

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The project reads the variable name from `config/config.yaml`, which currently points to `OPENAI_API_KEY`.

## Configuration

Update `config/config.yaml` before running the pipeline.

Example:

```yaml
project_name: resume_extraction

input:
  source_path: data/new_resumes

output:
  output_path: C:\path\to\your\output\folder

llm:
  api_key: "OPENAI_API_KEY"
  provider: openai
  model: gpt-5.4-mini

retry:
  max_attempts: 3
  initial_delay: 2
  max_delay: 30
```

### Important Notes

- `input.source_path` should point to a folder containing `.txt` resumes
- `output.output_path` is currently configured as an absolute Windows path in the repo, so you should change it to your local machine before running
- `llm.model` can be changed to any OpenAI model you want to use with this workflow

## Usage

### 1. Add resumes

Place candidate resumes as `.txt` files inside the configured input folder, for example:

```text
data/new_resumes/
|-- CAND008.txt
|-- CAND009.txt
`-- CAND010.txt
```

### 2. Run the pipeline

```bash
python main.py
```

### 3. Check outputs

For each run, the system creates a timestamped output folder like:

```text
<output_path>/<project_name>_YYYYMMDD_HHMMSS/
|-- raw/
|-- parsed/
|-- logs/
`-- results_YYYYMMDD_HHMMSS.xlsx
```

## Output Files

The pipeline generates:

- `raw/<candidate_id>_raw.json` - full raw structured API response
- `parsed/<candidate_id>_parsed.json` - cleaned structured candidate data
- `results_<run_id>.xlsx` - combined extraction results for all candidates
- `logs/logs.md` - run summary including total, success, failed, and execution time
- `logs/error_logs.xlsx` - export of candidates that failed during processing

## Example Use Cases

- resume screening prototypes
- recruiter workflow automation
- HR analytics experiments
- learning structured extraction with LLMs
- converting unstructured resumes into tabular data

## Limitations

- Only `.txt` resumes are supported right now
- The quality of extraction depends on resume formatting and model performance
- Some fields may be missing if they are not clearly present in the resume text
- The current output path is machine-specific until updated in the config
- `requirements.txt` contains many packages beyond the core runtime needs of this project

## Future Improvements

- add support for PDF and DOCX resumes
- build a lightweight web UI
- add unit tests
- support CSV export
- add confidence scoring and validation checks

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Author

Built as a learning project for structured resume data extraction using Python and LLMs.
