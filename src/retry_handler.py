import time

from openai import (
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    InternalServerError
)

RETRYABLE_ERRORS = (
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    InternalServerError
)

def call_with_retry(
        api_function,
        client,
        system_prompt,
        user_prompt,
        response_format,
        model,
        max_attempts = 3,
        initial_delay = 2,
        max_delay = 30,
):
    for attempt in range(1, max_attempts + 1):
        try:
            print(f'API attempt: {attempt}')

            result = api_function(
                client,
                system_prompt,
                user_prompt,
                response_format,
                model)

            return result

        except RETRYABLE_ERRORS as e:
            if attempt == max_attempts:
                print('All retry attempts are exhausted!')
                raise

            delay = min(
                initial_delay * (2 ** (attempt - 1), max_delay)
                )

            print(f"API Error: {e}")
            print(f'Retrying after {delay} seconds...')

            time.sleep(delay)