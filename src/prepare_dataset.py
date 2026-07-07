import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

fake = pd.read_csv(os.path.join(DATA_DIR, "Fake.csv"))
true = pd.read_csv(os.path.join(DATA_DIR, "True.csv"))

# Take 3000 samples from each class
fake = fake.sample(n=3000, random_state=42)
true = true.sample(n=3000, random_state=42)

fake["label"] = 0
true["label"] = 1

dataset = pd.concat([fake, true]).sample(frac=1, random_state=42)

dataset.to_csv(
    os.path.join(DATA_DIR, "news_dataset.csv"),
    index=False
)

print("Dataset Created Successfully")
print("Total Samples:", len(dataset))