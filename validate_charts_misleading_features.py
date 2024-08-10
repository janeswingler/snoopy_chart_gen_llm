import json

def validate_non_zero_baseline(chart):
    if chart['misleading'] and chart['misleading_feature'] == "Non-Zero Baseline":
        if chart['y_axis_start'] == 0:
            return f"Chart {chart['id']} failed: Non-Zero Baseline feature not applied correctly."
    elif not chart['misleading'] and chart['y_axis_start'] != 0:
        return f"Chart {chart['id']} failed: Non-misleading chart with non-zero y-axis start."
    return None

def validate_inconsistent_time_intervals(chart):
    if chart['misleading'] and chart['misleading_feature'] == "Inconsistent Time Intervals":
        if len(chart['data']) <= 2:
            return f"Chart {chart['id']} failed: Not enough data points for Inconsistent Time Intervals."
        x_values = [dp["x"] for dp in chart['data']]
        if len(x_values) != len(set(x_values)):
            return f"Chart {chart['id']} failed: Duplicate x values found."
    return None

def validate_non_sum_to_100(chart):
    if chart['misleading'] and chart['misleading_feature'] == "Non-Sum to 100":
        total_value = sum(dp["value"] for dp in chart["data"] if dp["value"] is not None)
        if total_value == 100:
            return f"Chart {chart['id']} failed: Total value of pie chart segments is 100."
    return None

def validate_charts(input_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    processed_graphs = data.get("graphs", [])
    errors = []

    for chart in processed_graphs:
        if chart['misleading_feature'] == "Non-Zero Baseline":
            error = validate_non_zero_baseline(chart)
        elif chart['misleading_feature'] == "Inconsistent Time Intervals":
            error = validate_inconsistent_time_intervals(chart)
        elif chart['misleading_feature'] == "Non-Sum to 100":
            error = validate_non_sum_to_100(chart)
        else:
            error = None

        if error:
            errors.append(error)

    if errors:
        print(f"Validation failed for the following charts:\n" + "\n".join(errors))
    else:
        print("All charts validated successfully.")

def main():
    input_file = '_.json'  # Researcher to adjust as necessary

    validate_charts(input_file)

if __name__ == "__main__":
    main()


