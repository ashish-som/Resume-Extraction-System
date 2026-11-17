from openai import OpenAI

def call_llm(
        client,
        system_prompt,
        user_prompt,
        response_format,
        model
):
    response = client.chat.completions.parse(
        model = model,
        messages =[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': user_prompt
            }
        ],
        response_format = response_format
    )

    message = response.choices[0].message

    if message.refusal:
        raise RuntimeError(
            f"Model refusal: {message.refusal}"
        )

    if message.parsed is None:
        raise RuntimeError(
            "No parsed response returned by the model"
        )

    return response