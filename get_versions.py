import io
import json
import os

import urllib3
import gzip

from src.client_config import ClientConfig

config = ClientConfig()

config_file = os.path.join(".pyupdater", "config.pyu")

def get_dict_from_url():
    name = config.UPDATE_URLS[0] + "versions.gz"
    f = urllib3.PoolManager().request('GET', name)
    if f.status != 200:
        print("Remote Version not found")
        return {}
    else:
        g = gzip.open(io.BytesIO(f.data))
        return json.load(g)

with open(config_file, "rb") as f:
    config_data = json.load(f)
remote_data = get_dict_from_url()
if "updates" in remote_data:
   config_data["version_meta"] = get_dict_from_url()
print(json.dumps(config_data), indent=4, sort_keys=True)
with open(config_file, "w") as outfile:
    json.dump(config_data, outfile, indent=4, sort_keys=True)
