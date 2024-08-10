import os
import json
import random
import matplotlib.pyplot as plt
import seaborn as sns

def load_combined_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def get_random_style():
    fonts = ['Arial', 'Times New Roman', 'Comic Sans MS', 'Verdana', 'Courier New',
             'Georgia', 'Garamond', 'Tahoma', 'Trebuchet MS', 'Impact']
    markers = ["o", "s", "D", "^", "v", "<", ">", "p", "*", "X"]
    palettes = ["deep", "muted", "bright", "pastel", "dark", "colorblind", "viridis", "plasma", "inferno", "magma",
                "cividis", "cubehelix", "hsv"]
    colors = ["#000000", "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
              "#bcbd22", "#17becf"]
    backgrounds = ["#f0f0f0", "#e6e6e6", "#cccccc", "#b3b3b3"]

    style = {
        "font": random.choice(fonts),
        "marker": random.choice(markers),
        "palette": random.choice(palettes),
        "font_size": random.randint(10, 14),
        "title_size": random.randint(16, 22),
        "label_size": random.randint(12, 18),
        "line_width": random.uniform(1, 3),
        "marker_size": random.uniform(5, 10),
        "title_color": random.choice(colors),
        "xlabel_color": random.choice(colors),
        "ylabel_color": random.choice(colors),
        "title_bold": random.choice([True, False]),
        "xlabel_bold": random.choice([True, False]),
        "ylabel_bold": random.choice([True, False]),
        "background_color": "#ffffff" if random.random() < 0.5 else random.choice(backgrounds)
    }
    return style

def generate_line_graphs(data, output_dir, start_index):
    os.makedirs(output_dir, exist_ok=True)

    for i, graph in enumerate(data["graphs"]):
        if i < start_index:
            continue

        try:
            style = get_random_style()
            sns.set(style="whitegrid")
            plt.figure(figsize=(10, 6))
            plt.rcParams["font.family"] = style["font"]
            plt.rcParams["font.size"] = style["font_size"]

            x = [point["x"] for point in graph["data"]]
            y = [point["y"] for point in graph["data"]]

            palette = sns.color_palette(style["palette"], len(x))
            for j in range(len(x)):
                plt.plot(x, y, linestyle='-', linewidth=style["line_width"],
                         marker=style["marker"], markersize=style["marker_size"], color=palette[j % len(palette)])

            plt.title(graph.get("title", ""), fontsize=style["title_size"], color=style["title_color"],
                      fontweight='bold' if style["title_bold"] else 'normal')
            plt.xlabel(graph.get("x_label", ""), fontsize=style["label_size"], color=style["xlabel_color"],
                       fontweight='bold' if style["xlabel_bold"] else 'normal')
            plt.ylabel(graph.get("y_label", ""), fontsize=style["label_size"], color=style["ylabel_color"],
                       fontweight='bold' if style["ylabel_bold"] else 'normal')

            plt.gca().set_facecolor(style["background_color"])

            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{graph.get('id', random.randint(0, 10000))}.png"))
            plt.close()
        except Exception as e:
            print(f"Failed to generate graph with ID {graph.get('id')}: {e}")
            continue

def main():
    input_file = "_.json" # Researcher to adjust as necessary
    output_dir = "_" # Researcher to adjust as necessary
    start_index = 0 # Specify the starting index here

    data = load_combined_json(input_file)
    generate_line_graphs(data, output_dir, start_index)

if __name__ == "__main__":
    main()



