import json

def remove_error_charts(input_file, error_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    with open(error_file, 'r') as errfile:
        errors = json.load(errfile)['errors']

    filtered_charts = [chart for chart in data['graphs'] if chart['id'] not in errors]

    with open(output_file, 'w') as outfile:
        json.dump({"graphs": filtered_charts}, outfile, indent=4)

    print(f"Removed {len(errors)} charts with parsing errors. Saved the cleaned data to {output_file}.")

def main():
    input_file = '_.json'  # Input file with all generated charts
    error_file = '_.json'  # File with parsing errors
    output_file = '_.json'  # Output file with cleaned charts

    remove_error_charts(input_file, error_file, output_file)

if __name__ == "__main__":
    main()
