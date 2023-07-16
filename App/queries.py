def tempWithtime(bucket, time):
    return f'from(bucket: "{bucket}")\
  |> range(start:-{time}h)\
  |> filter(fn: (r) => r["_measurement"] == "airSensors")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> filter(fn: (r) => r["sensor_id"] == "TLM0100" or r["sensor_id"] == "TLM0101")'


def humidityWithtime(bucket, time):
    return f'from(bucket: "{bucket}")\
  |> range(start:-{time}h)\
  |> filter(fn: (r) => r["_measurement"] == "airSensors")\
  |> filter(fn: (r) => r["_field"] == "humidity")\
  |> filter(fn: (r) => r["sensor_id"] == "TLM0100" or r["sensor_id"] == "TLM0101")'


def coWithtime(bucket, time):
    return f'from(bucket: "{bucket}")\
  |> range(start:-{time}h)\
  |> filter(fn: (r) => r["_measurement"] == "airSensors")\
  |> filter(fn: (r) => r["_field"] == "co")\
  |> filter(fn: (r) => r["sensor_id"] == "TLM0100" or r["sensor_id"] == "TLM0101")'
