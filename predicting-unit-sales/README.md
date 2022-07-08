## Architecture Diagram

![eds-2-new drawio (2)](https://user-images.githubusercontent.com/18354771/164086931-8604f20e-ac4f-4635-8de7-c1769997b83c.png)

## MLFlow Model Serving

First, you'll need to run a [notebook](xgb_time_series_all_stores.ipynb) to export a model directory. Then, run the following:

```
mlflow models serve -m models/XGB_Time_Series_All_Stores
```

The inference server will run at http://127.0.0.1:5000 and accept JSON payloads to generate predictions. 

Example request:

```
curl --location --request POST 'http://127.0.0.1:5000/invocations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "columns": ["year", "week", "A", "B", "C", "D", "E", "avg_oil_price"],
    "data": [[2013.0, 1.0, 0, 0, 1, 0, 0, 93.07]]
}'
```

Response:
```
[
    16156.001953125
]
```
