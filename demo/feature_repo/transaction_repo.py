from datetime import timedelta
import pandas as pd
from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    PushSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float64, Int64
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)


spending = Entity(name="spending", join_keys=["id"])

spending_source = PostgreSQLSource(
    name="spend",
    query="SELECT * FROM transaction",
    timestamp_field="window_end",
    created_timestamp_column="created_ts",
)


spend_fv_inferred = FeatureView(
    name="total_spend_inferred",
    entities=[spending],
    ttl=timedelta(hours=1),
    online=True,
    source=spending_source,
)


input_request = RequestSource(
    name="vals_to_add",
    schema=[
        Field(name="val_to_add", dtype=Int64),
        Field(name="val_to_add_2", dtype=Int64),
    ],
)


@on_demand_feature_view(
    sources=[spend_fv_inferred, input_request],
    schema=[
        Field(name="total_plus_val1", dtype=Float64),
        Field(name="total_plus_val2", dtype=Float64),
    ],
)
def spend_fv(inputs: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["total_plus_val1"] = inputs["total"] + inputs["val_to_add"]
    df["total_plus_val2"] = inputs["total"] + inputs["val_to_add_2"]
    return df


spending_service = FeatureService(
    name="spending_service",
    features=[spend_fv, spend_fv_inferred],
)

spending_push_source = PushSource(
    name="spending_push_source",
    batch_source=spending_source,
)

spend_fresh_fv = FeatureView(
    name="total_fresh_spend",
    entities=[spending],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total", dtype=Float64),
    ],
    online=True,
    source=spending_push_source,
)


@on_demand_feature_view(
    sources=[spend_fresh_fv, input_request],
    schema=[
        Field(name="total", dtype=Float64),
        Field(name="total_plus_val1", dtype=Float64),
        Field(name="total_plus_val2", dtype=Float64),
    ],
)
def spend_fresh_on_demand_fv(inputs: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["total"] = inputs["total"]
    df["total_plus_val1"] = inputs["total"] + inputs["val_to_add"]
    df["total_plus_val2"] = inputs["total"] + inputs["val_to_add_2"]
    return df


spending_fresh_service = FeatureService(
    name="spending_fresh_service",
    features=[spend_fresh_fv, spend_fresh_on_demand_fv],
)
