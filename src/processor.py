import os
import time
from pathlib import Path
from datetime import datetime

from src.data_loader import load_data
from src.models import ScreenResume
from src.prompt_builder import system_prompt, build_prompt
from src.llm_client import call_llm
from src.retry_handler import call_with_retry
from src.data_saver import (
    save_json, 
    save_run_logs, 
    parse_and_save
)


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

print(f'RUN ID: {run_id}')


def processor(config):
    # Start rxecution timer

    start_time = time.perf_counter()
    run_date = datetime.now().astimezone().strftime('%Y-%m-%d')

    errors = []
    data = []
    processed = []

    project_name = config['project_name']
    source_path = config['input']['source_path']
    output_dir = config['output']['output_path']
    
    output_path = f"{output_dir}/{project_name}_{run_id}"
    raw_path = f"{output_path}/raw"
    parsed_path = f"{output_path}/parsed"
    logs_path = f"{output_path}/logs"

    provider = config['llm']['provider']
    model = config['llm']['model']
    client = config['client']

    max_attempts = config['retry']['max_attempts']
    initial_delay = config['retry']['initial_delay']
    max_delay = config['retry']['max_delay']

    # Create output folders
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(raw_path, exist_ok=True)
    os.makedirs(parsed_path, exist_ok=True)


    # Get/Load the resumes
    resume_files = sorted(
        Path(source_path).glob(
            f"*.txt"
        )
    )

    if not resume_files:
        raise FileNotFoundError("No resume files are found!")


    # Process Resumes

    for file_path in resume_files:

        cand_id = file_path.stem

        print(f"\nProcessing ID: {cand_id}")

        processed.append(cand_id)

        try:

            # Load Resume
            text = load_data(file_path=file_path)

            # Build Prompt
            user_prompt = build_prompt(resume_text=text)

            # Call API with retry
            response = call_with_retry(
                api_function=call_llm,
                client=client,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=ScreenResume,
                model=model,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay
            )


            # Save raw api response
            raw_dump = response.model_dump(mode='json')

            save_json(
                output_path=raw_path,
                file_name=f"{cand_id}_raw.json",
                data=raw_dump
                )


            # Extract parsed response
            parsed_obj = response.choices[0].message.parsed

            if parsed_obj is None:
                raise ValueError("Parsed response is empty.")

            parsed_dump = parsed_obj.model_dump(mode='json')

            # Save parsed response in json format separately
            save_json(
                output_path=parsed_path,
                file_name=f"{cand_id}_parsed.json",
                data=parsed_dump
            )

            parsed_dump['cand_id'] = cand_id

            data.append(parsed_dump)

            print(f"Successfuly processed: {cand_id}")
        
        except Exception as e:
            print(f'ERROR in {cand_id}: {e}')

            errors.append({
                'candidate_id': cand_id,
                'error':str(e)
            })

    # Export daa to excel
    export_error = None

    try:
        print('\nSaving Excel Output')
        parse_and_save(
            output_path=output_path,
            file_name=f"results_{run_id}",
            data=data
        )

        parse_and_save(
            output_path=logs_path,
            file_name=f'error_logs',
            data=errors
        )
    except Exception as e:
        export_error = str(e)
        print(f'ERRORS while saving the excel files: {e}')

    # Calculate total execution time
    end_time = time.perf_counter()

    total_minutes = round((end_time - start_time)/60, 2)

    # Prepare run details
    run_details ={
        'run_id':run_id,
        'date':run_date,
        'provider':provider,
        'model':model,
        'total':len(processed),
        'successful':len(data),
        'failed':len(errors),
        'execution_time':f"{total_minutes} minutes",
        'status': 'successful' if export_error is None else 'failed'
    }

    # Save Logs
    print('!Saving Logs')
    save_run_logs(
        output_path=logs_path,
        log_file_name=f"logs.md",
        run_details=run_details
        )

    print('\nPipeline is completed!')

    print(f"Total Resume Processed: {run_details['total']}")
    print(f"Successful: {run_details['successful']}")
    print(f"Failed: {run_details['failed']}")
    print(f"Execution Time: {run_details['execution_time']}")

    if export_error:
        raise RuntimeError(
            f"Failed to save excel output: {export_error}"
        )

