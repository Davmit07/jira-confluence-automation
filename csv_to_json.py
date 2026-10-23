import csv
import json
from pathlib import Path
from typing import Union


def csv_to_json(csv_path: Union[str, Path], json_path: Union[str, Path]) -> None:
    """Convert a CSV file with a header row to a JSON array of records."""
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        records = list(csv.DictReader(csv_file))

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(records, json_file, indent=2, ensure_ascii=False)
        json_file.write("\n")