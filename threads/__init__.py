import os
import torch

REPO_PATH = "cache"

if not os.path.exists(REPO_PATH):
    os.mkdir(REPO_PATH)

torch.hub.set_dir(REPO_PATH)

# # check if images folder exists
# # if not create it
# IMAGES_PATH = "images"
# if not os.path.exists(IMAGES_PATH):
#     os.mkdir(IMAGES_PATH)

# # check if images.json exists
# # if not create it
# IMAGES_JSON_PATH = "images/images.json"
# if not os.path.exists(IMAGES_JSON_PATH):
#     data = {
#         "cigarette": [],
#     }
    
#     with open(IMAGES_JSON_PATH, "w", encoding="utf-8") as images_json:
#         json.dump(data, images_json, indent=4)