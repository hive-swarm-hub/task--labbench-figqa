#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/images
echo "Downloading LabBench FigQA..."
python3 << 'PY'
from datasets import load_dataset
import json, pathlib, random

random.seed(42)
ds = load_dataset('futurehouse/lab-bench', 'FigQA', split='train')

out = pathlib.Path('data/test.jsonl')
with out.open('w') as f:
    for i, row in enumerate(ds):
        # Save image
        img_path = f'data/images/{i:04d}.jpg'
        row['figure'].save(img_path)

        # Shuffle choices, track correct answer
        choices = [row['ideal']] + row['distractors']
        random.shuffle(choices)
        correct_letter = chr(65 + choices.index(row['ideal']))

        f.write(json.dumps({
            'question': row['question'],
            'choices': choices,
            'answer': correct_letter,
            'image_path': img_path,
        }) + '\n')

print(f'Wrote {len(ds)} problems to {out}')
PY
echo "Done. $(wc -l < data/test.jsonl) problems in data/test.jsonl"
