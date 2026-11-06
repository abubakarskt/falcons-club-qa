"""Ask a sample Falcons Club question and validate the model's JSON response."""

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
PROMPT_PATH = ROOT / "prompts" / "qa_prompt.txt"
QUESTION = "Where does the club meet?"


def load_documents():
    documents = []
    for path in sorted(DATA_DIR.glob("*.txt")):
        documents.append(f"--- {path.name} ---\n{path.read_text(encoding='utf-8').strip()}")
    if not documents:
        raise RuntimeError(f"No .txt documents found in {DATA_DIR}")
    return "\n\n".join(documents)


def ask_model(prompt):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set the OPENAI_API_KEY environment variable before running this script.")

    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": "Follow the user's instructions exactly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    request = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach the OpenAI API: {exc.reason}") from exc

    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("The API response did not contain a chat message.") from exc


def main():
    template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = template.format(question=QUESTION, documents=load_documents())
    raw_response = ask_model(prompt)
    try:
        answer = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model did not return valid JSON: {raw_response}") from exc

    if not isinstance(answer, dict) or not isinstance(answer.get("answer"), str) or "source" not in answer:
        raise RuntimeError('Expected a JSON object with "answer" and "source" fields.')

    print(json.dumps(answer, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
