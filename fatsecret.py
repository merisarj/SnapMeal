#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com/",
    api_key="SOS2WPF4re41QmdVH2gt"
)

custom_config = InferenceConfiguration(confidence_threshold=0.01, iou_threshold=0.3)

with CLIENT.use_configuration(custom_config):
    your_image = Image.open("static/uploads/captured-image.jpg")
    result = CLIENT.infer(your_image, model_id="food-bxkvw/3")

labels = [prediction["class"] for prediction in result["predictions"]]

# In[17]:


import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = 'e6ce66a8cc7f4887a208bc5f2f71dfc3'
CLIENT_SECRET = '97805a872c5a496ababe2489cb24d7d0'
TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'

response = requests.post(
    TOKEN_URL,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    data={'grant_type': 'client_credentials'}
)

response.raise_for_status()
access_token = response.json().get('access_token')

print("Access Token:", access_token)


# In[18]:


SEARCH_URL = 'https://platform.fatsecret.com/rest/server.api'

headers = {
    'Authorization': f'Bearer {access_token}'
}

search_term = labels[0]

params = {
    'method': 'foods.search',
    'format': 'json',
    'search_expression': search_term
}

response = requests.get(SEARCH_URL, headers=headers, params=params)
data = response.json()


# In[19]:


import re
import os

# Normalize search term (lowercase)
base_term = search_term.lower()

# Generate both singular or plural form
if base_term.endswith('s'):
    alt_term = base_term[:-1]
else:
    alt_term = base_term + 's'

# Regex to match singular or plural (whole word)
pattern = re.compile(rf'\b({re.escape(base_term)}|{re.escape(alt_term)})\b', re.IGNORECASE)

foods = data.get('foods', {}).get('food', [])

for food in foods:
    name = food.get('food_name', 'Unknown')

    # Match either form
    if not pattern.search(name):
        continue

    desc = food.get('food_description', '')

    # Extract macros
    calories = re.search(r'Calories:\s*([\d\.]+)kcal', desc)
    fat = re.search(r'Fat:\s*([\d\.]+)g', desc)
    carbs = re.search(r'Carbs:\s*([\d\.]+)g', desc)
    protein = re.search(r'Protein:\s*([\d\.]+)g', desc)

    # Create result dictionary
    result = {
        'food_name': name,
        'calories': float(calories.group(1)) if calories else None,
        'fat': float(fat.group(1)) if fat else None,
        'carbs': float(carbs.group(1)) if carbs else None,
        'protein': float(protein.group(1)) if protein else None
    }

    # Format result as a text block
    text_entry = (
        f"Food: {result['food_name']}\n"
        f"  Calories: {result['calories']} kcal\n"
        f"  Fat: {result['fat']} g\n"
        f"  Carbs: {result['carbs']} g\n"
        f"  Protein: {result['protein']} g\n"
        "--------------------------\n"
    )

    # Append to the text file
    with open('output.txt', 'w') as f:
        f.write(text_entry)

    # Optional: print output
    print(text_entry)

    break  # Remove this if you want to save multiple matches

