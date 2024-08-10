import json

def validate_chart_data(input_file, validation_output_file, error_output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    charts = data.get("graphs", [])
    invalid_charts = []

    for chart in charts:
        has_error = False

        if not chart["title"]:
            print(f"Chart {chart['id']} has an empty or null title.")
            has_error = True
        if not chart["source"]:
            print(f"Chart {chart['id']} has an empty or null source.")
            has_error = True
        if chart["visualisation_type"] in ["bar", "time series bar", "time series line"]:
            if not chart["x_label"]:
                print(f"Chart {chart['id']} has an empty or null x_label.")
                has_error = True
            if not chart["y_label"]:
                print(f"Chart {chart['id']} has an empty or null y_label.")
                has_error = True

        if has_error:
            invalid_charts.append(chart)

    with open(error_output_file, 'r') as errorfile:
        error_data = json.load(errorfile)
        error_charts = error_data.get("errors", [])

    all_invalid_charts = invalid_charts + error_charts

    with open(validation_output_file, 'w') as outfile:
        json.dump({"invalid_charts": all_invalid_charts}, outfile, indent=4)

    print(f"Validation complete. {len(all_invalid_charts)} invalid charts found. Results saved to {validation_output_file}.")

def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    validation_output_file = '_.json'  # Researcher to adjust as necessary
    error_output_file = '_.json'  # Researcher to adjust as necessary

    validate_chart_data(input_file, validation_output_file, error_output_file)

if __name__ == "__main__":
    main()
