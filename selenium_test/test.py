
import re
import json


response = '{"a": "data"}'
response_json = json.loads(response)
print(response_json["a"])
