import json
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

def create_caption_dataset(input_file, output_file, start_index=0):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    processed_graphs = data.get("graphs", [])
    for idx, graph in enumerate(processed_graphs[start_index:], start=start_index):
        image_id = graph['id']

        if graph["visualisation_type"] == "bar":
            instruction = "Considering only y axis start point, is this chart misleading? Explain."
        elif graph["visualisation_type"] == "pie":
            instruction = "Considering only sum of segments, is this chart misleading? Explain."
        elif graph["visualisation_type"] == "time series bar":
            instruction = "Considering the intervals between data points on the x-axis, is this chart misleading? If so, explain."
        elif graph["visualisation_type"] == "time series line":
            instruction = "Is this chart misleading? Explain."
        else:
            continue


        prompt = f"Given data visualization:\n\n{json.dumps(graph)}\n\nInstruction: {instruction}\nResponse (No extraneous text, headings, or text formatting in response):"
        caption = generate_llm_response(prompt)

        graph['caption'] = caption


        if (idx + 1) % 10 == 0:
            with open(output_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print(f"Processed {idx + 1} files. Intermediate results saved.")

    # Final save
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Processed all files. All results saved.")

def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    output_file = '_.json'  # Researcher to adjust as necessary

    create_caption_dataset(input_file, output_file)

if __name__ == "__main__":
    main()
