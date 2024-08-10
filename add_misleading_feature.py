import json
import random

def add_non_zero_baseline(chart):
    min_y = min(dp["y"] for dp in chart["data"])
    y_axis_start = int(random.uniform(0.2 * min_y, 0.8 * min_y))
    chart['misleading'] = True
    chart['misleading_feature'] = "Non-Zero Baseline"
    chart['y_axis_start'] = y_axis_start
    return chart

def add_inconsistent_time_intervals(chart):
    def remove_data_points(data):
        num_points = len(data)
        if num_points <= 3:
            return data
        if num_points == 4 or num_points == 5:
            index_to_remove = random.randint(1, num_points - 2)
            data.pop(index_to_remove)
        elif num_points >= 6:
            indices_to_remove = random.sample(range(1, num_points - 1), 2)
            for index in sorted(indices_to_remove, reverse=True):
                data.pop(index)
        return data

    chart['data'] = remove_data_points(chart['data'])
    if len(chart['data']) <= 3:
        return None
    chart['misleading'] = True
    chart['misleading_feature'] = "Inconsistent Time Intervals"
    return chart

def add_non_sum_to_100(chart):
    total_value = sum(dp["value"] for dp in chart["data"] if dp["value"] is not None)
    if total_value == 100:
        chart["data"][0]["value"] += random.choice([-5, 5])
    chart['misleading'] = True
    chart['misleading_feature'] = "Non-Sum to 100"
    return chart

def process_charts(input_file, output_file, feature):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    processed_graphs = data.get("graphs", [])
    total_graphs = len(processed_graphs)
    half_graphs = total_graphs // 2

    for idx, chart in enumerate(processed_graphs):
        if idx < half_graphs:
            # Misleading chart
            if feature == 'Non-Zero Baseline' and chart["visualisation_type"] == "bar":
                chart = add_non_zero_baseline(chart)
            elif feature == 'Inconsistent Time Intervals' and chart["visualisation_type"] in ["bar", "time series line"]:
                chart = add_inconsistent_time_intervals(chart)
            elif feature == 'Non-Sum to 100' and chart["visualisation_type"] == "pie":
                chart = add_non_sum_to_100(chart)
        else:
            # Non-misleading chart
            chart['misleading'] = False
            chart['misleading_feature'] = "None"

    for chart in processed_graphs:
        if 'misleading' not in chart:
            chart['misleading'] = False
        if 'misleading_feature' not in chart:
            chart['misleading_feature'] = "None"
        if 'y_axis_start' not in chart and chart["visualisation_type"] in ["bar", "time series bar"]:
            chart['y_axis_start'] = 0

    with open(output_file, 'w') as outfile:
        json.dump({"graphs": processed_graphs}, outfile, indent=4)

    print(f"Processed all charts. All results saved to {output_file}.")

def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    output_file = '_.json'  # Researcher to adjust as necessary

    # Specify the misleading feature to apply: 'Non-Zero Baseline', 'Inconsistent Time Intervals', 'Non-Sum to 100'
    feature = '_'

    process_charts(input_file, output_file, feature)

if __name__ == "__main__":
    main()

