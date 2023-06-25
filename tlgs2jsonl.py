import pandas as pd
import json
import argparse

parser = argparse.ArgumentParser(description='Convert TLGS database dump to JSONL')
parser.add_argument('source', metavar='input', type=str, nargs=1,
                    help='source CSV file path')
parser.add_argument('output', metavar='output', type=str, nargs=1,
                    help='output JSONL file path')

args = parser.parse_args()
input_path = args.source[0]
output_path = args.output[0]

df = pd.read_csv(input_path, dtype=str)

# Deduplicate pages as the same page can be in multiple URLs
# Also filter out small pages
texts = {}
for i, row in df.iterrows():
    h = row["raw_content_hash"]
    b = row["content_body"]

    # Filter out bad, unwanted data
    if isinstance(b, float) or isinstance(b, int): continue
    # Page too small. Likely unintresting data
    if len(b) < 512: continue

    # Deduplicate page data
    if h in texts:
        if not b in texts[h]: texts[h] += [b]
    else:
        texts[h] = [b]

f = open(output_path, "w")
for _, t in texts.items():
    for txt in t:
        j = {'text': txt}
        s = json.dumps(j, indent=None)
        f.write(s + '\n')
f.close()
