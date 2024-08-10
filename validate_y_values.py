import json
from collections import Counter

def check_for_duplicate_y_values(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    processed_graphs = data.get("graphs", [])
    duplicates_list = []
    cleaned_graphs = []

    for chart in processed_graphs:
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            y_values = [dp["y"] for dp in chart["data"]]
            duplicates = [item for item, count in Counter(y_values).items() if count > 1]

            if duplicates:
                print(f"Chart {chart['id']} has duplicate y values: {duplicates}")
                duplicates_list.append(chart)
            else:
                cleaned_graphs.append(chart)
        elif chart["visualisation_type"] == "pie":
            values = [dp["value"] for dp in chart["data"]]
            duplicates = [item for item, count in Counter(values).items() if count > 1]

            if duplicates:
                print(f"Chart {chart['id']} has duplicate values: {duplicates}")
                duplicates_list.append(chart)
            else:
                cleaned_graphs.append(chart)

    with open(output_file, 'w') as outfile:
        json.dump({"duplicate_y_values": duplicates_list}, outfile, indent=4)

    print(f"Results saved to {output_file}")
    return cleaned_graphs


def check_for_null_y_values(graphs, output_file):
    null_y_values_list = []
    cleaned_graphs = []

    for chart in graphs:
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            y_values = [dp["y"] for dp in chart["data"]]
            if any(value is None or value == "" for value in y_values):
                print(f"Chart {chart['id']} has null or empty y values: {y_values}")
                null_y_values_list.append(chart)
            else:
                cleaned_graphs.append(chart)
        elif chart["visualisation_type"] == "pie":
            values = [dp["value"] for dp in chart["data"]]
            if any(value is None or value == "" for value in values):
                print(f"Chart {chart['id']} has null or empty values: {values}")
                null_y_values_list.append(chart)
            else:
                cleaned_graphs.append(chart)

    with open(output_file, 'w') as outfile:
        json.dump({"null_y_values": null_y_values_list}, outfile, indent=4)

    print(f"Null or empty value results saved to {output_file}")
    return cleaned_graphs


def main():
    input_file = 'final_bars_for_captioning.json'  # Researcher to adjust as necessary
    output_file_duplicates = 'duplicate_y_values_list.json'  # Output file for charts with duplicate y values
    output_file_nulls = 'null_y_values_list.json'  # Output file for charts with null or empty y values
    output_file_cleaned = 'output_file.json'  # Researcher to adjust as necessary

    cleaned_graphs = check_for_duplicate_y_values(input_file, output_file_duplicates)
    cleaned_graphs = check_for_null_y_values(cleaned_graphs, output_file_nulls)

    with open(output_file_cleaned, 'w') as outfile:
        json.dump({"graphs": cleaned_graphs}, outfile, indent=4)

    print(f"Cleaned charts saved to {output_file_cleaned}")


if __name__ == "__main__":
    main()
