import json
from collections import Counter

def check_for_duplicate_x_labels(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    processed_graphs = data.get("graphs", [])
    duplicates_list = []
    cleaned_graphs = []

    for chart in processed_graphs:
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            x_labels = [dp["x"] for dp in chart["data"]]
            duplicates = [item for item, count in Counter(x_labels).items() if count > 1]

            if duplicates:
                print(f"Chart {chart['id']} has duplicate x labels: {duplicates}")
                duplicates_list.append(chart)
            else:
                cleaned_graphs.append(chart)
        elif chart["visualisation_type"] == "pie":
            categories = [dp["category"] for dp in chart["data"]]
            duplicates = [item for item, count in Counter(categories).items() if count > 1]

            if duplicates:
                print(f"Chart {chart['id']} has duplicate categories: {duplicates}")
                duplicates_list.append(chart)
            else:
                cleaned_graphs.append(chart)

    with open(output_file, 'w') as outfile:
        json.dump({"duplicate_x_categories": duplicates_list}, outfile, indent=4)

    print(f"Results saved to {output_file}")
    return cleaned_graphs


def check_for_null_x_labels(graphs, output_file):
    null_x_labels_list = []
    cleaned_graphs = []

    for chart in graphs:
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            x_labels = [dp["x"] for dp in chart["data"]]
            if any(label is None or label == "" for label in x_labels):
                print(f"Chart {chart['id']} has null or empty x labels: {x_labels}")
                null_x_labels_list.append(chart)
            else:
                cleaned_graphs.append(chart)
        elif chart["visualisation_type"] == "pie":
            categories = [dp["category"] for dp in chart["data"]]
            if any(category is None or category == "" for category in categories):
                print(f"Chart {chart['id']} has null or empty categories: {categories}")
                null_x_labels_list.append(chart)
            else:
                cleaned_graphs.append(chart)

    with open(output_file, 'w') as outfile:
        json.dump({"null_x_categories": null_x_labels_list}, outfile, indent=4)

    print(f"Null or empty label results saved to {output_file}")
    return cleaned_graphs


def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    output_file_duplicates = '_.json'  # Output file for charts with duplicate x labels
    output_file_nulls = '_.json'  # Output file for charts with null or empty x labels
    output_file_cleaned = '_.json'  # Researcher to adjust as necessary

    cleaned_graphs = check_for_duplicate_x_labels(input_file, output_file_duplicates)
    cleaned_graphs = check_for_null_x_labels(cleaned_graphs, output_file_nulls)

    with open(output_file_cleaned, 'w') as outfile:
        json.dump({"graphs": cleaned_graphs}, outfile, indent=4)

    print(f"Cleaned charts saved to {output_file_cleaned}")


if __name__ == "__main__":
    main()

