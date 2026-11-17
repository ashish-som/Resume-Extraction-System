from pathlib import Path

def load_data(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() != '.txt':
        raise ValueError("Only .txt files are supported")

    text = file_path.read_text(encoding='utf-8')

    if not text.strip():
        raise ValueError(f'Resume file is empty: {file_path}')

    return text