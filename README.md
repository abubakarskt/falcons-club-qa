# Falcons Club Q&A

A small Flask starter project for answering questions about a fictional Falcons Club using its rules, event schedule, and membership FAQ. It includes a reusable JSON-output prompt and a command-line script that sends the sample question and club documents to the OpenAI API.

## Requirements

- Python 3.11+
- An OpenAI API key with API access (the API may be billed separately from ChatGPT)

## Install

```bash
git clone https://github.com/abubakarskt/falcons-club-qa.git
cd falcons-club-qa
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install packages and configure your key:

```bash
pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in your shell. For example:

```bash
# macOS/Linux
export OPENAI_API_KEY="your-api-key"

# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"
```

Optionally set `OPENAI_MODEL` to choose another chat-completions-compatible model; the default is `gpt-4o-mini`.

## Run the web app

```bash
python app.py
```

Open <http://localhost:5000>.

## Run the prompt test

```bash
python test_qa.py
```

The script loads all three text documents, asks where the club meets, requests a JSON object with `answer` and `source`, validates those fields, and prints the JSON. `source` includes the document name and a supporting excerpt. The script reports an error if the model response is not valid JSON or is missing either required field.

## Project layout

```text
.
├── app.py
├── data/
│   ├── club_rules.txt
│   ├── event_schedule.txt
│   └── membership_faq.txt
├── prompts/
│   └── qa_prompt.txt
├── templates/
│   └── index.html
├── test_qa.py
└── requirements.txt
```

The club, schedule, and contact details are fictional sample content for this demo.
