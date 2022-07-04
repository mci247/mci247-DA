from page_data import page_info
import db_connect
import numpy as np
import pandas as pd
import math
import requests
from datetime import datetime, timedelta
from pip import main
impo


def dataHandle(df):
    for i in range(6):
        page_id = page_info['page_' + str(i + 1)]['page_id']
        page_number = page_info['page_' + str(i + 1)]['page_number']
        page_size = page_info['page_' + str(i + 1)]['page_size']
        since = page_info['page_' + str(i + 1)]['since']
        curr_time = datetime.datetime.now() + timedelta(seconds=3)
        until = int(time.mktime(curr_time.timetuple()))
        access_token = page_info['page_' + str(i + 1)]['access_token']

        res = requests.get(
            f'https://pages.fm/api/public_api/v1/pages/{page_id}/page_customers/?page_id={page_id}&access_token={access_token}&since={since}&until={until}&page_number={page_number}&page_size={page_size}')
        data = res.json()
        total_records = data['total']
        total_page = math.ceil(total_records/page_size)

        for i in range(1, total_page + 1):
            curr_res = requests.get(
                f'https://pages.fm/api/public_api/v1/pages/{page_id}/page_customers/?page_id={page_id}&access_token={access_token}&since={since}&until={until}&page_number={page_number}&page_size={page_size}')
            customers = curr_res.json()['customers']
            page_number += 1
            for idx, each in enumerate(customers):
                if "lives_in" in each.keys():
                    if each['recent_orders'] is not None:
                        for order in each['recent_orders']:
                            df = df.append({"name": each['name'], "gender": each['gender'], "address": each['lives_in'],
                                            "mobile": order['phone_number'], "source_lead": "BOT", "note": "OD", "page_id": page_id}, ignore_index=True)
                    else:
                        df = df.append({"name": each['name'], "gender": each['gender'], "address": each['lives_in'],
                                        "mobile": each['phone_numbers'], "source_lead": "BOT", "note": "FB", "page_id": page_id}, ignore_index=True)
                else:
                    if each['recent_orders'] is not None:
                        for order in each['recent_orders']:
                            df = df.append({"name": each['name'], "gender": each['gender'], "address": "",
                                            "mobile": order['phone_number'], "source_lead": "BOT", "note": "OD", "page_id": page_id}, ignore_index=True)
                    else:
                        df = df.append({"name": each['name'], "gender": each['gender'], "address": "",
                                        "mobile": each['phone_numbers'], "source_lead": "BOT", "note": "FB", "page_id": page_id}, ignore_index=True)
            break
    return df


def main():
    mobiles = np.asarray(db_connect.getMobile())
    count = 0

    df = pd.DataFrame(columns=["name", "gender", "address",
                               "mobile", "source_lead", "note", "page_id"])
    leads_df = dataHandle(df)
    leads_df = leads_df[df["mobile"].map(lambda r: r != [])]
    leads_df = leads_df[df["mobile"].notna()]
    leads_df = leads_df.fillna("")

    for index, row in df.iterrows():
        name = row["name"]
        mobile = row["mobile"]
        gender = row["gender"]
        address = row["address"]
        source_lead = row["source_lead"]
        note = row["note"]
        page_id = row["page_id"]

        values = (name, mobile, gender, address, source_lead, note, page_id)

        if mobile not in mobiles:
            db_connect.insertData(name, mobile, gender,
                                  address, source_lead, note, page_id)
            count += 1
            print("Ops something went wrong!!! Your phone number existed in MCI DB")
    db_connect.database.commit()
    db_connect.database.close()
    print(f"I just imported {count} rows to MCI DB")


if __name__ == "__main__":
    main()

# print(dataHandle(df))
