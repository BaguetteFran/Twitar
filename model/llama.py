import sqlite3
import json
from transformers import pipeline
import torch

# Step 1: Convert SQLite Database to JSON
def sqlite_to_json(db_path, table_name):
    """
    Extracts data from a SQLite database table and returns it as a JSON object.

    Args:
        db_path (str): Path to the SQLite database.
        table_name (str): Name of the table to extract data from.

    Returns:
        dict: The table data as a list of dictionaries.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Convert rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Close the database connection
    conn.close()

    return data

# Step 2: Process JSON with Llama Model
def process_with_llama(json_data, model_id, task_prompt, device="cpu"):
    """
    Processes JSON data using a Llama model.

    Args:
        json_data (dict): JSON data to process.
        model_id (str): Hugging Face model ID.
        task_prompt (str): Task description for the model.
        device (str): Device to run the model on ("cpu" or "cuda").

    Returns:
        str: Model-generated output.
    """
    # Convert JSON to a formatted string
    json_string = json.dumps(json_data, indent=2)

    # Build the model prompt
    prompt = f"{task_prompt}\n\n{json_string}"

    # Load the model pipeline
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
    )

    # Generate output
    outputs = pipe(
        prompt,
        max_new_tokens=512,  # Adjust token limit as needed
        temperature=0.7,     # Adjust temperature for response creativity
    )

    return outputs[0]["generated_text"]

# Step 3: Callable Function
def sqlite_to_llama(db_path, table_name, model_id, task_prompt, device="cpu"):
    """
    Combines the SQLite-to-JSON conversion and Llama processing.

    Args:
        db_path (str): Path to the SQLite database.
        table_name (str): Table to query in the SQLite database.
        model_id (str): Hugging Face model ID.
        task_prompt (str): Task description for the model.
        device (str): Device to run the model on ("cpu" or "cuda").

    Returns:
        str: Model-generated output.
    """
    # Convert SQLite table to JSON
    json_data = sqlite_to_json(db_path, table_name)

    # Process the JSON data with Llama
    return process_with_llama(json_data, model_id, task_prompt, device)


# import sqlite_to_llama

# # Define inputs
# database_path = "example.db"  # Path to your SQLite database
# table_name = "tweets"         # Table to export
# model_id = "meta-llama/Llama-3.2-3B-Instruct"  # Llama model ID
# task_prompt = "Analyze the following JSON data and summarize key insights:"  # Task for the model

# # Call the function
# result = sqlite_to_llama.sqlite_to_llama(
#     db_path=database_path,
#     table_name=table_name,
#     model_id=model_id,
#     task_prompt=task_prompt,
#     device="cuda"  # or "cpu"
# )

# # Print the result
# print("Llama Model Output:")
# print(result)
