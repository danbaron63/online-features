import csv
import random
import json


def load_data(path):
    data = []
    with open(path, "r") as f:
        csvreader = csv.reader(f, delimiter=",")
        keys = next(csvreader)
        for line in csvreader:
            rec = dict()
            for i, val in enumerate(line):
                rec[keys[i]] = val
            data.append(rec)
    return data


def get_random_record(path):
    data = load_data(path)
    i = random.randrange(0, len(data), 1)
    return data[i]


def get_random_record_json(path):
    return json.dumps(get_random_record(path))


if __name__ == "__main__":
    print(
        get_random_record_json("data/file1.csv")
    )
