import requests
import json
import pandas as pd
import math

page_id = 102791862223216
page_number = 1
since = 1622632226
until = 1654168226
page_size = 100
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aW1lc3RhbXAiOjE2NTQxNjYzODQsImlkIjoiMTAyNzkxODYyMjIzMjE2In0.gIQ54vohc_CHOr2HF5em9PaCWbfKhGq3KQ2Tmb_KD_Q'

res = requests.get(
    f'https://pages.fm/api/public_api/v1/pages/{page_id}/page_customers/?page_id={page_id}&access_token={access_token}&since={since}&until={until}&page_number={page_number}&page_size={page_size}')

data = res.json()
total_records = data['total']
total_page = math.ceil(total_records/page_size)

name_arr = []
gender_arr = []
mobile_arr = []
address_arr = []
for i in range(1, total_page + 1):
    curr_res = requests.get(
        f'https://pages.fm/api/public_api/v1/pages/{page_id}/page_customers/?page_id={page_id}&access_token={access_token}&since={since}&until={until}&page_number={page_number}&page_size={page_size}')
    customers = curr_res.json()['customers']
    for customer in customers:
        name_arr.append(customer['name'])
        gender_arr.append(customer['gender'])
        mobile_arr.append(customer['phone_numbers'])
        if customer['recent_orders'] is not None:
            for order in customer['recent_orders']:
                if order['phone_number'] not in customer['phone_numbers']:
                    customer['phone_numbers'].append(order['phone_number'])

    df = pd.DataFrame(data={
                      'name': name_arr, 'gender': gender_arr, 'mobile': mobile_arr})
    page_number += 1

df = df[df['mobile'].map(lambda d: len(d)) > 0]
print(df)
