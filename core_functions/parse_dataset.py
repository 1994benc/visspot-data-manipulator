import csv
from flask import abort, jsonify
from admin import dataset_ref
from auth_required import get_user_id
import pandas as pd


def parse_dataset(dataset_id, page=1, pagination=1, page_size=48):
    try:
        doc = dataset_ref.document(dataset_id).get()
        if (doc.exists):
            data = doc.to_dict()

            if (data["public"] == False or data["public"] == None):
                # Will throw an error if user is not logged in
                user_id = get_user_id()
                if (user_id != data["author"]):
                    abort(
                        500, description="You are not the owner of this private dataset")

            parsed_data = switch_types(
                data["type"], data["url"], dataset_data=data)

            if (pagination == 1):
                split = [parsed_data[i:i+page_size]
                         for i in range(0, len(parsed_data), page_size)]
                # print(split)
                # Index out of range
                if (page > len(split)):
                    return {"total_size": len(split), "data": []}
                return {"total_size": len(split), "data": split[page-1]}
            else:
                # No pagination
                # Return the entire dataset
                return {"total_size": len(parsed_data), "data": parsed_data}
        else:
            print("Not exist")
            return {"total_size": 0, "data": []}
    except Exception as e:
        abort(500, description=e)


def switch_types(type, url, dataset_data):
    if (type == "csv"):
        return parse_csv(url)
    elif (type == "json"):
        return parse_json(url)
    elif (type == "dsv"):
        return parse_dsv(url, dataset_data)
    elif (type == "tsv"):
        return parse_tsv(url)
    else:
        return []


def parse_csv(url):
    df = pd.read_csv(url)
    # df_list =list(df.T.to_dict().values())
    # print(df_list)
    df_list = df.to_dict(orient='records')
    return df_list


def parse_json(url):
    df = pd.read_json(url)
    df_list = df.to_dict(orient='records')
    return list(df_list)


def parse_dsv(url, dataset_data):
    df = pd.read_table(url, delimiter=dataset_data['delim'])
    df_list = list(df.to_dict(orient='records'))
    return df_list


def parse_tsv(url):
    df = pd.read_csv(url, sep='\t')
    df_list = df.to_dict(orient='records')
    return list(df_list)
