import json
import random
from openai import OpenAI
from config import API_KEY

client = OpenAI(api_key=API_KEY)

GPT_MODEL = "gpt-4o"

domains = [
    "Finance",
    "Sales and Marketing",
    "Healthcare",
    "Education",
    "Technology",
    "Retail",
    "Government and Public Policy",
    "Environment",
    "Sports",
    "Logistics and Supply Chain",
    "Human Resources",
    "Real Estate",
    "Manufacturing",
    "Travel and Tourism",
    "Agriculture",
    "Energy",
    "Media and Entertainment",
    "Non-Profit and Social Services"
]

visualisation_types = ["bar", "time series bar", "time series line", "pie"]

def generate_llm_response(prompt):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a creative thinker."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.7,
    )
    return response.choices[0].message.content

def create_random_chart(num_charts, visualisation_type, start_num):
    charts = []
    for i in range(start_num, start_num + num_charts):
        domain = random.choice(domains)
        chart = {
            "id": f"{visualisation_type.replace(' ', '')}{i}",
            "title": "",
            "visualisation_type": visualisation_type,
            "source": "",
            "domain": domain,
        }

        if visualisation_type in ["bar", "time series bar", "time series line"]:
            chart["x_label"] = ""
            chart["y_label"] = ""

        charts.append(chart)
    return charts

def generate_context_for_charts(charts, output_file, error_file):
    errors = []
    for idx, chart in enumerate(charts):
        vis_type_for_llm = chart["visualisation_type"]

        if chart["visualisation_type"] == "pie":
            fields = "title and source"
            json_structure = """
{
    "title": "",
    "source": ""
}
"""
        else:
            fields = "title, source, x_label, and y_label for a single series"
            json_structure = """
{
    "title": "",
    "source": "",
    "x_label": "",
    "y_label": ""
}
"""

        prompt = f"""
Given the following {vis_type_for_llm} JSON object and the domain '{chart['domain']}', provide values for the fields: {fields}.

JSON object:
{json.dumps(chart, indent=4)}

Return only the JSON object. No extraneous text.
{json_structure}
"""

        context_response = generate_llm_response(prompt)

        try:
            context_data = json.loads(context_response)
        except json.JSONDecodeError:
            error_message = f"Error parsing JSON response for chart {chart['id']}"
            print(error_message)
            errors.append(chart['id'])
            context_data = json.loads(json_structure)

        chart['title'] = context_data.get("title", "")
        chart['source'] = context_data.get("source", "")
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            chart['x_label'] = context_data.get("x_label", "")
            chart['y_label'] = context_data.get("y_label", "")

        if (idx + 1) % 10 == 0:
            with open(output_file, 'w') as outfile:
                json.dump({"graphs": charts}, outfile, indent=4)
            print(f"Processed {idx + 1} charts. Intermediate results saved.")

    with open(output_file, 'w') as outfile:
        json.dump({"graphs": charts}, outfile, indent=4)

    with open(error_file, 'w') as errorfile:
        json.dump({"errors": errors}, errorfile, indent=4)

    print(f"Processed all charts. All results saved.")

def main():
    num_charts = 3000  # Number of charts to generate
    visualisation_type = 'bar'  # Specify the visualisation type here (e.g., 'bar', 'time series bar', 'time series line', 'pie')
    start_num = 1  # Specify the starting number for the IDs

    output_files = {
        "bar": '1.json',
        "time series bar": 'time_series_bar_dataset.json',
        "time series line": 'time_series_line_dataset.json',
        "pie": 'pie_dataset.json'
    }

    error_files = {
        "bar": 'parsing_errors_bar.json',
        "time series bar": 'parsing_errors_time_series_bar.json',
        "time series line": 'parsing_errors_time_series_line.json',
        "pie": 'parsing_errors_pie.json'
    }

    charts = create_random_chart(num_charts, visualisation_type, start_num)
    generate_context_for_charts(charts, output_files[visualisation_type], error_files[visualisation_type])

if __name__ == "__main__":
    main()




