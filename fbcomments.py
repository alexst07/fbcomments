#!/usr/bin/env python3

import urllib
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import argparse

ACCESS_TOKEN = ""
num_comments = 0

# get facebook page id
def get_page_id(page):
    params = urlencode({
        'access_token': ACCESS_TOKEN})

    req = urlopen('https://graph.facebook.com/v2.10/' + page + '?' + params)

    return req.read()


# mount object id, 'xxxx_yyyy'
def mount_object_id(page_json, post_id):
    json_data = json.loads(page_json.decode("utf-8"))
    return json_data["id"] + '_' + post_id


# list comments from given object id
def comments_request(id):
    params = urlencode({
        'access_token': ACCESS_TOKEN})
    req = urlopen('https://graph.facebook.com/v2.10/' + id +
        '/comments?' + params)

    content = req.read()
    json_content = json.loads(content.decode("utf-8"))
    data = json_content["data"]

    if not data:
        return data

    paging = json_content['paging']

    while "next" in paging:
        req = urlopen(json_content['paging']['next'])
        content = req.read()
        json_content = json.loads(content.decode("utf-8"))
        data.extend(json_content["data"])
        paging = json_content['paging']

    return data


# recurive function to list all comments and return in json format
def list_comments(id, answers = False):
    data = comments_request(id)

    if answers:
        ret_json = ', \n"answers":[\n'
    else:
        ret_json = '{ "data":['

    has_data = False

    # iterate over all comments and find its answers
    for obj in data:
        global num_comments
        num_comments += 1
        print (str(num_comments) + " comments downloaded\r", end='')

        ret_json += '{\n'
        ret_json += '"from":"' + obj["from"]["name"] + '",\n'
        ret_json += '"from_id":"' + obj["from"]["id"] + '",\n'
        ret_json += '"message":"' + obj["message"] + '"'

        # list all answers recursively
        ret_json += list_comments(obj["id"], True)

        ret_json += '},\n'
        has_data = True

    if answers:
        ret_json = (ret_json[:-2] if has_data else ret_json) + ']\n'
    else:
        ret_json = ret_json[:-2] + ']}\n'

    return ret_json


def main():
    global ACCESS_TOKEN

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', action='store',
                    dest='access_token',
                    help='access token',
                    required=True)

    parser.add_argument('-p', action='store',
                    dest='page_url',
                    help='facebook page url',
                    required=True)

    parser.add_argument('-i', action='store',
                    dest='post_id',
                    help='facebook post id',
                    required=True)

    parser.add_argument('-f', action='store',
                    dest='file_name',
                    help='output file',
                    required=True)

    parser.add_argument('--version', action='version',
                    version='%(prog)s 0.1')

    results = parser.parse_args()

    ACCESS_TOKEN = results.access_token

    obj_id = mount_object_id(get_page_id(results.page_url), results.post_id)

    res = list_comments(obj_id)
    open(results.file_name, "w+").write(res)
    print("\nDone!")


if __name__ == "__main__":
    main()
