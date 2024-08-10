import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from config import API_KEY

load_dotenv()

client = OpenAI(api_key=API_KEY)

GPT_MODEL = "gpt-4o"

def generate_llm_response(prompt):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a creative thinker."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.6,
    )
    return response.choices[0].message.content

def add_data_labels(input_file, output_file, error_file, start_index=0):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    errors = []
    processed_graphs = data.get("graphs", [])
    for idx, graph in enumerate(processed_graphs[start_index:], start=start_index):
        if graph["visualisation_type"] == "bar":
            num_data_points = random.randint(2, 10)
            instruction = f"Provide {num_data_points} x-axis data point labels for the single series bar chart."
        elif graph["visualisation_type"] == "time series bar":
            num_data_points = random.randint(2, 10)
            instruction = f"Provide {num_data_points} x-axis data point labels for the single series time series bar chart."
        elif graph["visualisation_type"] == "time series line":
            num_data_points = random.randint(2, 10)
            instruction = f"Provide {num_data_points} x-axis data point labels for the single series time series line chart."
        elif graph["visualisation_type"] == "pie":
            num_data_points = random.randint(2, 6)
            instruction = f"Provide {num_data_points} category labels for the pie chart."
        else:
            continue  # Skip if it's not a recognized chart type

        # Generate LLM response
        prompt = f"""
Given the following data visualization JSON object, {instruction}

JSON object:
{json.dumps(graph, indent=4)}

return only JSON object. no extraneous text. 
{{
    "data_labels": []
}}
"""
        context_response = generate_llm_response(prompt)

        try:
            context_data = json.loads(context_response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON response for graph {graph.get('id', 'unknown')}")
            errors.append(graph.get('id', 'unknown'))
            context_data = {"data_labels": []}

        data_labels = context_data.get("data_labels", [])
        if data_labels:
            if graph["visualisation_type"] == "pie":
                graph['data'] = [{"category": label, "value": None} for label in data_labels]
            else:
                graph['data'] = [{"x": label, "y": None} for label in data_labels]

        if (idx + 1) % 10 == 0:
            with open(output_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            with open(error_file, 'w') as errfile:
                json.dump({"errors": errors}, errfile, indent=4)
            print(f"Processed {idx + 1} files. Intermediate results saved.")

    # Final save
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    with open(error_file, 'w') as errfile:
        json.dump({"errors": errors}, errfile, indent=4)

    print(f"Processed all files. All results saved.")

def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    output_file = '_.json'  # Researcher to adjust as necessary
    error_file = '_.json'  # Researcher to adjust as necessary

    start_index = 0

    add_data_labels(input_file, output_file, error_file, start_index=start_index)

if __name__ == "__main__":
    main()




