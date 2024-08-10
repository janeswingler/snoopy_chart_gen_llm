import json

def validate_and_remove_charts(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    valid_charts = []
    removed_charts = []

    for chart in data['graphs']:
        caption = chart.get('caption', '').strip()
        if caption:
            valid_charts.append(chart)
        else:
            removed_charts.append(chart['id'])


    data['graphs'] = valid_charts
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Removed {len(removed_charts)} charts due to null or empty captions: {removed_charts}")

def main():
    input_file = '_.json'  # Input file with chart data
    output_file = '_.json'  # Output file after removal & validation

    validate_and_remove_charts(input_file, output_file)

if __name__ == "__main__":
    main()
