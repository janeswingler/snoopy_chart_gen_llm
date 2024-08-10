import os
import json
import random
from matplotlib import pyplot as plt
import seaborn as sns


FONT_NAMES = [
    'Arial', 'Times New Roman', 'Comic Sans MS', 'Verdana', 'Courier New',
    'Georgia', 'Garamond', 'Tahoma', 'Trebuchet MS', 'Impact'
]
FONT_SIZES = [12, 14, 16, 18, 20, 22, 24, 26]
FONT_WEIGHTS = ['normal', 'bold']
EDGE_COLORS = ['black', 'grey', 'white']
LINE_WIDTHS = [1, 2]

COLOR_PALETTES = [
    'deep', 'bright', 'pastel', 'dark', 'colorblind',
    'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
    'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu',
    'YlOrBr', 'YlOrRd', 'Spectral', 'coolwarm', 'cividis', 'cubehelix', 'gist_earth',
    'inferno', 'magma', 'plasma', 'rocket', 'turbo', 'twilight', 'viridis', 'vlag',
    'icefire'
]

def apply_random_style(elements):
    palette_name = random.choice(COLOR_PALETTES)
    palette = sns.color_palette(palette_name, len(elements[0]))

    edge_color = random.choice(EDGE_COLORS)
    line_width = random.choice(LINE_WIDTHS)

    for wedge, color in zip(elements[0], palette):
        wedge.set_facecolor(color)
        wedge.set_edgecolor(edge_color)
        wedge.set_linewidth(line_width)

    font_style = {
        'fontname': random.choice(FONT_NAMES),
        'fontsize': random.choice(FONT_SIZES),
        'weight': random.choice(FONT_WEIGHTS)
    }
    plt.title(plt.gca().get_title(), **font_style)

    for text in elements[1] + elements[2]:
        text.set_fontname(font_style['fontname'])
        text.set_fontsize(font_style['fontsize'])
        text.set_weight(font_style['weight'])

def plot_pie_chart(chart, output_dir):
    data = chart['data']
    labels = [item['category'] for item in data]
    sizes = [max(int(item['value']), 1) for item in data]

    fig, ax = plt.subplots(figsize=(random.uniform(10, 14), random.uniform(8, 12)))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%d%%', startangle=140)
    ax.set_title(chart['title'], pad=20)

    apply_random_style((wedges, texts, autotexts))

    source_font_style = {
        'fontname': random.choice(FONT_NAMES),
        'fontsize': random.choice(FONT_SIZES),
        'weight': random.choice(FONT_WEIGHTS)
    }
    plt.figtext(0.5, 0.02, f"Source: {chart['source']}", ha='center', **source_font_style)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{chart['id']}.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def main():
    input_file = '_.json'  # Researcher to adjust as necessary
    output_dir = '_'  # Researcher to adjust as necessary
    start_index = 0  # Specify the starting index here

    with open(input_file, 'r') as infile:
        data = json.load(infile)

    for idx, chart in enumerate(data['graphs'][start_index:], start=start_index):
        try:
            plot_pie_chart(chart, output_dir)
        except Exception as e:
            print(f"Error processing chart {chart['id']}: {e}")
            continue

if __name__ == "__main__":
    main()



