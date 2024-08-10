import os
import json
import pandas as pd
from datasets import Dataset, DatasetDict, Features, Image, Value, ClassLabel

def load_data(json_paths, image_dirs):
    all_data = []
    for json_path, image_dir in zip(json_paths, image_dirs):
        with open(json_path, 'r') as f:
            data = json.load(f)["graphs"]
            for item in data:
                image_path = os.path.join(image_dir, f"{item['id']}.png")
                if os.path.exists(image_path):
                    item['image'] = image_path
                    all_data.append(item)
                else:
                    print(f"Image not found: {image_path}, skipping this item.")
    df = pd.DataFrame(all_data)
    df.rename(columns={'visualisation_type': 'chart_type'}, inplace=True)
    return df

def split_data(df, train_ratio=0.8, val_ratio=0.1):
    df = df.sample(frac=1).reset_index(drop=True)
    train_end = int(train_ratio * len(df))
    val_end = int((train_ratio + val_ratio) * len(df))
    return df[:train_end], df[train_end:val_end], df[val_end:]

def create_datasets(train_df, val_df, test_df):
    features = Features({
        "id": Value("string"),
        "title": Value("string"),
        "image": Image(decode=True),
        "chart_type": Value("string"),
        "domain": Value("string"),
        "is_misleading": ClassLabel(names=["No", "Yes"]),
        "misleading_feature": Value("string"),
        "conversations": [
            {
                "query": Value("string"),
                "label": Value("string")
            }
        ]
    })

    train_dataset = Dataset.from_pandas(train_df, features=features)
    val_dataset = Dataset.from_pandas(val_df, features=features)
    test_dataset = Dataset.from_pandas(test_df, features=features)

    return train_dataset, val_dataset, test_dataset

def push_to_hf(repo_id, token, train_dataset, val_dataset, test_dataset):
    dataset_dict = DatasetDict({
        'train': train_dataset,
        'validation': val_dataset,
        'test': test_dataset
    })

    dataset_dict.save_to_disk("hf_dataset")
    dataset_dict.push_to_hub(repo_id, token=token)
    print("Dataset uploaded successfully!")

if __name__ == "__main__":
    repo_id = "_"  # Researcher to adjust as necessary
    token = "_"  # Researcher to adjust as necessary

    json_paths = ["_.json"]
    image_dirs = ["_"]

    df = load_data(json_paths, image_dirs)
    train_df, val_df, test_df = split_data(df)
    train_dataset, val_dataset, test_dataset = create_datasets(train_df, val_df, test_df)
    push_to_hf(repo_id, token, train_dataset, val_dataset, test_dataset)



