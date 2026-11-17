import os
from openai import OpenAI

from src.config_loader import load_config
from dotenv import load_dotenv

def main():

    try:

        # Load configuration file
        config = load_config(config_path="config/config.yaml")

        # Load environment variables
        load_dotenv()
        api_key= os.getenv(f"{config['llm']['api_key']}")

        client = OpenAI(api_key=api_key)

        config['client'] = client

        # Import processor and load config
        from src.processor import processor

        # Start pipeline
        processor(config=config)

    except Exception as e:
        print(f'Pipeline Failed: {e}')


if __name__ == '__main__':
    main()
    