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
            {"role": "system", "content": "You are a data visualization expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.6,
    )
    return response.choices[0].message.content

def add_y_data_values(input_file, output_file, error_file, start_index=0):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    errors = []
    processed_graphs = data.get("graphs", [])
    for idx, graph in enumerate(processed_graphs[start_index:], start=start_index):
        if graph["visualisation_type"] == "pie":
            for dp in graph["data"]:
                dp["value"] = None

            instruction = "Provide integer values for the categories ensuring the total sums to 100."
            prompt = f"""
Given the following data visualization JSON object, {instruction}

JSON object:
{json.dumps(graph, indent=4)}

return only JSON object. no extraneous text. 
{{
    "data": [
        {", ".join([f'{{"category": "{dp["category"]}", "value": ""}}' for dp in graph["data"]])}
    ]
}}
"""
        else:
            for dp in graph["data"]:
                dp["y"] = None

            instruction = "Provide integer y-values for the data points."
            prompt = f"""
Given the following data visualization JSON object, {instruction}

JSON object:
{json.dumps(graph, indent=4)}

return only JSON object. no extraneous text. 
{{
    "data": [
        {", ".join([f'{{"x": "{dp["x"]}", "y": ""}}' for dp in graph["data"]])}
    ]
}}
"""

        context_response = generate_llm_response(prompt)

        try:
            context_data = json.loads(context_response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON response for graph {graph.get('id', 'unknown')}")
            errors.append({"id": graph.get('id', 'unknown'), "error": "JSONDecodeError"})
            if graph["visualisation_type"] == "pie":
                context_data = {"data": [{"category": dp["category"], "value": random.randint(0, 100)} for dp in graph["data"]]}
            else:
                context_data = {"data": [{"x": dp["x"], "y": random.randint(0, 100)} for dp in graph["data"]]}

        y_data = context_data.get("data", [])
        if y_data and len(y_data) == len(graph['data']):
            for i, data_point in enumerate(graph['data']):
                if graph["visualisation_type"] == "pie":
                    data_point['value'] = y_data[i]['value']
                else:
                    data_point['y'] = y_data[i]['y']

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
    add_y_data_values(input_file, output_file, error_file, start_index=start_index)

if __name__ == "__main__":
    main()



