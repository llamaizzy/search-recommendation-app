import json
import pandas as pd

data = []
file = "/Users/Izzy/Downloads/meta_Electronics.jsonl"
with open(file, 'r') as f:
    for i, line in enumerate(f):
        item = json.loads(line.strip())

        data.append({
            "id": item.get("parent_asin"),
            "title": item.get("title"),
            "description": " ".join(item.get("description", [])),
            "categories": " ".join(item.get("categories", [])),
        })

        if i > 20000: # limit for speed
            break
df = pd.DataFrame(data)
df = df.dropna(subset=["title"])

# Save data
df.to_csv("data.csv", index=False)
print("✅ Saved to data.csv")