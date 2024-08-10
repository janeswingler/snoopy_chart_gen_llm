import os
import json

def create_processed_json(input_json, output_json, img_dir):
    with open(input_json, 'r') as infile:
        data = json.load(infile)

    processed_graphs = []
    for graph in data["graphs"]:
        if len(graph["data"]) > 1:
            if graph["visualisation_type"] == "bar":
                chart_type = "bar"
                queries = [
                    {
                        "query": "What is the range of the y-axis?",
                        "label": f"{min(item['y'] for item in graph['data'])} to {max(item['y'] for item in graph['data'])}"
                    },
                    {
                        "query": "What is the start of the y-axis?",
                        "label": str(graph.get("y_axis_start", ""))
                    }
                ]
            elif graph["visualisation_type"] == "time series bar":
                chart_type = "time series bar"
                queries = [
                    {
                        "query": "What are the points on the x-axis?",
                        "label": ", ".join(item['x'] for item in graph['data'])
                    },
                    {
                        "query": "Is this bar chart misleading? Explain",
                        "label": graph.get("caption", "")
                    }
                ]
            elif graph["visualisation_type"] == "time series line":
                chart_type = "time series line"
                queries = [
                    {
                        "query": "What are the points on the x-axis?",
                        "label": ", ".join(item['x'] for item in graph['data'])
                    },
                    {
                        "query": "Is this line chart misleading? Explain",
                        "label": graph.get("caption", "")
                    }
                ]
            elif graph["visualisation_type"] == "pie":
                chart_type = "pie"
                queries = [
                    {
                        "query": "What are the segments of the pie chart?",
                        "label": ", ".join(item['category'] for item in graph['data'])
                    },
                    {
                        "query": "What is the sum of the segments of the pie chart?",
                        "label": str(sum(int(item['value']) for item in graph['data']))
                    },
                    {
                        "query": "Is this pie chart misleading? Explain",
                        "label": graph.get("caption", "")
                    }
                ]
            else:
                continue

            processed_graph = {
                "id": graph["id"],
                "title": graph.get("title", ""),
                "image": os.path.join(img_dir, f"{graph['id']}.png"),
                "visualisation_type": chart_type,
                "domain": graph.get("domain", ""),
                "is_misleading": "Yes" if graph.get("misleading") else "No",
                "misleading_feature": graph.get("misleading_feature", ""),
                "conversations": queries
            }
            processed_graphs.append(processed_graph)

    with open(output_json, 'w') as outfile:
        json.dump({"graphs": processed_graphs}, outfile, indent=4)

if __name__ == "__main__":
    input_json = "_.json"  # Researcher to adjust as necessary
    output_json = "_.json"  # Researcher to adjust as necessary
    img_dir = "_"  # Researcher to adjust as necessary
    create_processed_json(input_json, output_json, img_dir)
    print(f"Processed JSON saved to {output_json}")


