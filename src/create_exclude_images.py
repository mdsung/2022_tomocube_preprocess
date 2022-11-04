import pandas as pd

MEAN_VALUE_LOW = 13370
MEAN_VALUE_HIGH = 13385

distribution = pd.read_csv("data/processed/distribution_metrics.csv")

lower_filter = distribution["value_mean"] < MEAN_VALUE_LOW
higher_filter = distribution["value_mean"] >= MEAN_VALUE_HIGH

result = distribution[lower_filter | higher_filter]
result.to_csv("data/processed/exclude_images.csv", index=False)
