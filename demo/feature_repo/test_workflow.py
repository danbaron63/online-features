from feast import FeatureStore
import requests
import json
from pprint import pprint


if __name__ == "__main__":
    store = FeatureStore(repo_path=".")
    entity_rows = [
        # {join_key: entity_value}
        {
            "id": 1,
            "val_to_add": 1000,
            "val_to_add_2": 2000,
        },
        {
            "id": 2,
            "val_to_add": 1001,
            "val_to_add_2": 2002,
        },
    ]
    features_to_fetch = [
        "spend_fresh_on_demand_fv:total",
        "spend_fresh_on_demand_fv:total_plus_val1",
        "spend_fresh_on_demand_fv:total_plus_val2",
    ]

    print("--- Retrieving features using SDK ---")
    returned_features = store.get_online_features(
        features=features_to_fetch,
        entity_rows=entity_rows,
    ).to_dict()
    for key, value in sorted(returned_features.items()):
        print(key, " : ", value)

    print("--- Retrieving features using endpoint ---")
    response = requests.post(
        "http://localhost:6566/get-online-features",
        data=json.dumps({
            "features": features_to_fetch,
            "entities": entity_rows
        })
    )
    pprint(json.loads(response.text))
