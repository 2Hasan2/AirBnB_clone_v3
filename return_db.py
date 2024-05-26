#!/usr/bin/python3
"""
starts a Flask web application
"""
import json
from models import storage
from models import *
from models.state import *

state_res = storage.all(State)
state_list = [state.to_dict() for state in state_res.values()]
json_string = json.dumps(state_list, indent=4)
print(json_string)

# for key, value in state_res.items():
#     json.dumps(value)
#     print("{}".format(value.to_dict()))
