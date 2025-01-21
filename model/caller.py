import sqlite_to_llama

# Define inputs
database_path = "/Users/kristianbanchs/Desktop/Twitar/data-tool/bluesky_posts_1.sqlite"  # Path to your SQLite database
table_name = "posts"         # Table to export
model_id = "meta-llama/Llama-3.2-3B-Instruct"  # Llama model ID
task_prompt = "Analyze the following JSON data and summarize key insights:"  # Task for the model

# Call the function
result = sqlite_to_llama.sqlite_to_llama(
    db_path=database_path,
    table_name=table_name,
    model_id=model_id,
    task_prompt=task_prompt,
    device="cuda"  # or "cpu"
)

# Print the result
print("Llama Model Output:")
print(result)
