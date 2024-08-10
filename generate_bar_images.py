import os
import json
import random
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


BAR_WIDTHS = [0.4, 0.6, 0.8]
FONT_NAMES = [
    'Arial', 'Times New Roman', 'Comic Sans MS', 'Verdana', 'Courier New',
    'Georgia', 'Garamond', 'Tahoma', 'Trebuchet MS', 'Impact'
]
FONT_SIZES = [12, 14, 16, 18, 20]
FONT_WEIGHTS = ['normal', 'bold']
EDGE_COLORS = ['black', 'grey', 'white']
LINE_WIDTHS = [1, 2]
EDGE_STYLES = [None, 'solid']
SOFT_BACKGROUND_COLORS = [
    '#f5f5f5', '#e6e6e6', '#e0ffff', '#ffffe0', '#e6ffe6',
    '#ffebcd', '#f0f8ff', '#e0ffff', '#f5fffa', '#fff5ee'
]
SOFT_LIGHT_COLORS = [
    '#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a'
]


SEABORN_STYLES = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']


COLOR_PALETTES = [
    'deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind',
    'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
    'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu',
    'YlOrBr', 'YlOrRd', 'Spectral', 'coolwarm', 'cividis', 'cubehelix', 'gist_earth',
    'inferno', 'magma', 'plasma', 'rocket', 'turbo', 'twilight', 'viridis', 'vlag',
    'icefire'
]

BACKGROUND_STYLES = ['single_line', 'solid_color', 'solid_with_lines', 'gradient']

def apply_random_style(chart_type, elements):
    if random.random() < 0.1:
        apply_media_style(elements)
        return

    sns.set_style(random.choice(SEABORN_STYLES))
    palette_name = random.choice(COLOR_PALETTES)
    palette = sns.color_palette(palette_name)

    background_style = random.choice(BACKGROUND_STYLES)
    if background_style == 'single_line':
        plt.gca().set_facecolor(random.choice(SOFT_BACKGROUND_COLORS))
        plt.gca().axhline(y=0, color=random.choice(EDGE_COLORS), linewidth=random.choice(LINE_WIDTHS))
    elif background_style == 'solid_color':
        plt.gca().set_facecolor(random.choice(SOFT_BACKGROUND_COLORS))
    elif background_style == 'solid_with_lines':
        plt.gca().set_facecolor(random.choice(SOFT_BACKGROUND_COLORS))
        for y in np.arange(0, 1, 0.1):
            plt.gca().axhline(y=y, color=random.choice(EDGE_COLORS), linewidth=random.choice(LINE_WIDTHS))
    elif background_style == 'gradient':
        ax = plt.gca()
        ax.set_facecolor('none')
        light_color = random.choice(SOFT_LIGHT_COLORS)
        z = np.linspace(0, 1, 256).reshape(-1, 1)
        z = np.concatenate([z, z], axis=1)
        plt.imshow(z, aspect='auto', cmap=plt.get_cmap('Blues'), extent=ax.get_xlim() + ax.get_ylim(), zorder=-1, alpha=0.3)

    if chart_type == 'bar':
        bar_width = random.choice(BAR_WIDTHS)
        edge_color = random.choice(EDGE_COLORS)
        line_width = random.choice(LINE_WIDTHS)
        edge_style = random.choice(EDGE_STYLES)
        bar_colors = palette[:len(elements)]

        add_hatch = random.random() < 0.5
        hatch = random.choice(['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']) if add_hatch else None

        for bar, color in zip(elements, bar_colors):
            bar.set_color(color)
            if edge_style:
                bar.set_edgecolor(edge_color)
                bar.set_linewidth(line_width)
            else:
                bar.set_edgecolor(color)
                bar.set_linewidth(0)
            bar.set_width(bar_width)
            if hatch:
                bar.set_hatch(hatch)
    elif chart_type == 'line':
        elements.set_linewidth(random.choice(LINE_WIDTHS))
        elements.set_color(random.choice(palette))
    elif chart_type == 'pie':
        for i, wedge in enumerate(elements[0]):
            wedge.set_edgecolor(random.choice(EDGE_COLORS))
            wedge.set_linewidth(random.choice(LINE_WIDTHS))
            wedge.set_facecolor(random.choice(palette))

    font_style = {
        'fontname': random.choice(FONT_NAMES),
        'fontsize': random.choice(FONT_SIZES),
        'weight': random.choice(FONT_WEIGHTS)
    }
    plt.title(plt.gca().get_title(), **font_style)
    plt.xlabel(plt.gca().get_xlabel(), **font_style)
    plt.ylabel(plt.gca().get_ylabel(), **font_style)

    ax = plt.gca()
    for tick in ax.get_xticklabels():
        tick.set_fontname(font_style['fontname'])
        tick.set_fontsize(font_style['fontsize'])
        tick.set_weight(font_style['weight'])
    for tick in ax.get_yticklabels():
        tick.set_fontname(font_style['fontname'])
        tick.set_fontsize(font_style['fontsize'])
        tick.set_weight(font_style['weight'])

    plt.gcf().autofmt_xdate()

def apply_media_style(elements):
    media_style = random.choice([1, 2, 3])

    if media_style == 1:
        plt.gcf().set_facecolor('#000080')
        plt.gca().set_facecolor('#000080')
        bar_colors = ['#FFFF00'] * len(elements)
        plt.gca().tick_params(axis='x', colors='#FFFF00')
        plt.gca().tick_params(axis='y', colors='#FFFF00')
        plt.gca().spines['bottom'].set_color('#FFFF00')
        plt.gca().spines['left'].set_color('#FFFF00')
        plt.gca().spines['top'].set_color('#FFFF00')
        plt.gca().spines['right'].set_color('#FFFF00')
        plt.xlabel(plt.gca().get_xlabel(), color='#FFFF00')
        plt.ylabel(plt.gca().get_ylabel(), color='#FFFF00')
        plt.title(plt.gca().get_title(), color='#FFFF00')

    elif media_style == 2:
        plt.gcf().set_facecolor('#D3D3D3')
        plt.gca().set_facecolor('#D3D3D3')
        bar_colors = ['#87CEFA'] * len(elements)
        plt.gca().tick_params(axis='x', colors='#000080')
        plt.gca().tick_params(axis='y', colors='#000080')
        plt.gca().spines['bottom'].set_color('#000080')
        plt.gca().spines['left'].set_color('#000080')
        plt.gca().spines['top'].set_color('#000080')
        plt.gca().spines['right'].set_color('#000080')
        plt.xlabel(plt.gca().get_xlabel(), color='#000080')
        plt.ylabel(plt.gca().get_ylabel(), color='#000080')
        plt.title(plt.gca().get_title(), color='#000080')

    elif media_style == 3:
        plt.gcf().set_facecolor('#ADD8E6')
        plt.gca().set_facecolor('#ADD8E6')
        bar_colors = ['#D3D3D3'] * len(elements)
        plt.gca().tick_params(axis='x', colors='#000080')
        plt.gca().tick_params(axis='y', colors='#000080')
        plt.gca().spines['bottom'].set_color('#808080')
        plt.gca().spines['left'].set_color('#808080')
        plt.gca().spines['top'].set_color('#808080')
        plt.gca().spines['right'].set_color('#808080')
        plt.xlabel(plt.gca().get_xlabel(), color='#000080')
        plt.ylabel(plt.gca().get_ylabel(), color='#000080')
        plt.title(plt.gca().get_title(), color='#000080')

    for bar, color in zip(elements, bar_colors):
        bar.set_color(color)
        bar.set_edgecolor(color)
        bar.set_linewidth(0)

    font_style = {
        'fontname': random.choice(FONT_NAMES),
        'fontsize': random.choice(FONT_SIZES),
        'weight': random.choice(FONT_WEIGHTS)
    }
    plt.xlabel(plt.gca().get_xlabel(), **font_style)
    plt.ylabel(plt.gca().get_ylabel(), **font_style)
    plt.title(plt.gca().get_title(), **font_style)

    ax = plt.gca()
    for tick in ax.get_xticklabels():
        tick.set_fontname(font_style['fontname'])
        tick.set_fontsize(font_style['fontsize'])
        tick.set_weight(font_style['weight'])
    for tick in ax.get_yticklabels():
        tick.set_fontname(font_style['fontname'])
        tick.set_fontsize(font_style['fontsize'])
        tick.set_weight(font_style['weight'])

def plot_bar_chart(chart, output_dir):
    data = chart['data']
    categories = [item['x'] for item in data]
    values = [item['y'] for item in data]
    y_start = chart['y_axis_start'] if chart['misleading_feature'] == 'Non-Zero Baseline' else 0

    fig, ax = plt.subplots(figsize=(random.uniform(10, 14), random.uniform(8, 12)))
    bar_plot = ax.bar(categories, values)
    ax.set_title(chart['title'], pad=20)
    ax.set_xlabel(chart['x_label'], labelpad=20)
    ax.set_ylabel(chart['y_label'], labelpad=20)
    ax.set_ylim(bottom=y_start)

    y_ticks = ax.get_yticks()
    if y_start not in y_ticks:
        y_ticks = np.append(y_ticks, y_start)
    y_ticks = sorted(y_ticks)

    if y_start != 0 and 0 in y_ticks:
        y_ticks = [yt for yt in y_ticks if yt != 0]

    y_interval = max((max(values) - y_start) // 5, 1)
    y_ticks = range(y_start, max(values) + y_interval, y_interval)
    plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.25)
    ax.set_yticks(y_ticks)

    apply_random_style('bar', bar_plot)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

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
    start_num = 0 # Starting index

    with open(input_file, 'r') as infile:
        data = json.load(infile)

    filtered_charts = [chart for chart in data['graphs'] if int(chart['id'].replace('bar', '')) >= start_num]

    for chart in filtered_charts:
        plot_bar_chart(chart, output_dir)

if __name__ == "__main__":
    main()
