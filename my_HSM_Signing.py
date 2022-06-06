import json
import requests
import time
import hashlib
import base64
import os
import sys


from io import StringIO
from my_signing_file_digest_process_window import SigningProgressWindow
from time import sleep

PATH = os.path.dirname(os.path.realpath(__file__))


def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


def get_auth(api_endpoint, api_key, signing_process_window):
    url = "{}/sys/v1/session/auth".format(api_endpoint)

    payload = {}
    headers = {'Authorization': 'Basic {}'.format(api_key)}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 401:
        signing_process_window.terminal_output.configure(text="Wrong API key, unable to authenticate close session "
                                                              "please check log file",
                                                         font=("Roboto", 8, "bold"))
    response_json = response.json()
    response_print = json.dumps(response_json)
    print("get_auth{}".format(response_print))
    return response_json["access_token"]


def gen_auth_request_for_sign(token, api_endpoint, key, hash_value, alg, signing_process_window):
    url = "{}/sys/v1/approval_requests".format(api_endpoint)
    payload = json.dumps({
        "method": "POST",
        "operation": "/crypto/v1/sign",
        "body": {
            "key": {
                "name": "{}".format(key)
            },
            "hash_alg": "{}".format(alg),
            "data": "{}".format(hash_value)
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 404:
        signing_process_window.terminal_output.configure(text="Wrong key name or hash value, close session and check"
                                                              "log file",
                                                         font=("Roboto", 8, "bold"))
    response_json = response.json()["request_id"]
    response_print = json.dumps(response_json)
    print("gen_auth_request_for_sign{}".format(response_print))
    return response_json


def check_request_status(token, api_endpoint):
    url = "{}/sys/v1/approval_requests".format(api_endpoint)
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()
    response_print = json.dumps(response_json)
    print("check_request_status{}".format(response_print))
    return response_json


def get_sign(api_endpoint, token, request_id, signing_process_window):
    url = "{}/sys/v1/approval_requests/{}/result".format(api_endpoint, request_id)

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 401:
        signing_process_window.terminal_output.configure(text="An Error occurred during signing please check log file",
                                                         font=("Roboto", 10, "bold"))
    response_json = response.json()
    response_print = json.dumps(response_json)
    print("get_sign{}".format(response_print))
    return response_json


def hash_file(filename, operation):
    """"This function returns the SHA-256 hash
   of the file passed into it"""

    # make a hash object
    if operation == 'SHA2-256':
        h = hashlib.sha256()

    if operation == 'SHA3-256':
        h = hashlib.sha3_256()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.digest()


def signing_digest(api_endpoint, api_key, in_data, out_data, key_name, operation):
    signing_process_window = SigningProgressWindow()

    fh = open("{}".format(in_data), 'rb')
    result_digest = bytearray(fh.read)
    hash_value = base64.b64encode(result_digest).decode("utf-8")
    api_key = api_key
    api_endpoint = api_endpoint
    key = key_name

    signing_process_window.terminal_output.configure(text="SHA2-signing process started",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(0)
    signing_process_window.update_idletasks()
    sleep(1)

    if operation == 'SHA3-256':
        alg = 'Sha3256'
    if operation == 'SHA2-256':
        alg = 'Sha256'
    token = get_auth(api_endpoint, api_key)
    request_id = gen_auth_request_for_sign(token, api_endpoint, key, hash_value, alg)

    match = {'status': 'PENDING'}
    signing_process_window.terminal_output.configure(text="SHA2-signing pending for quorum approval",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(0.66)
    signing_process_window.update_idletasks()
    sleep(2)

    while match['status'] == 'PENDING':
        status = check_request_status(token, api_endpoint)
        match = next(d for d in status if d['request_id'] == request_id)
        time.sleep(0.25)
    print('request approved getting signature')

    signing_process_window.terminal_output.configure(text="SHA2-signing approved",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(1)
    signing_process_window.update_idletasks()
    full_status_string = get_sign(api_endpoint, token, request_id)

    file_name = str(in_data)
    file_ending = file_name.split(".")
    file_ending = file_ending[-1]

    with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
        f.write('Request response:')

    append_new_line('{}_signature.{}'.format(in_data, file_ending), "{}".format(full_status_string))


def signing(api_endpoint, api_key, in_data, out_data, key_name, operation):
    signing_process_window = SigningProgressWindow()
    result = hash_file(in_data, operation)
    result_digest = bytearray(result)
    hash_value = base64.b64encode(result_digest).decode("utf-8")
    api_key = api_key
    api_endpoint = api_endpoint
    key = key_name

    signing_process_window.terminal_output.configure(text="SHA2-signing process started",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(0)
    signing_process_window.update_idletasks()
    sleep(2)

    if operation == 'SHA3-256':
        alg = 'Sha3256'
    if operation == 'SHA2-256':
        alg = 'Sha256'
    token = get_auth(api_endpoint, api_key, signing_process_window)
    request_id = gen_auth_request_for_sign(token, api_endpoint, key, hash_value, alg, signing_process_window)

    signing_process_window.terminal_output.configure(text="SHA2-digest",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(0.33)
    signing_process_window.update_idletasks()
    sleep(2)

    print("my digest:{}".format(hash_value))
    print("SHA3-Digest Generation")

    match = {'status': 'PENDING'}
    signing_process_window.terminal_output.configure(text="SHA2-signing pending for quorum approval",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(0.66)
    signing_process_window.update_idletasks()
    sleep(2)

    while match['status'] == 'PENDING':
        status = check_request_status(token, api_endpoint, signing_process_window)
        match = next(d for d in status if d['request_id'] == request_id)
        time.sleep(0.25)
    print('request approved getting signature')

    signing_process_window.terminal_output.configure(text="SHA2-signing approved",
                                                     font=("Roboto", 10, "bold"))
    signing_process_window.progress_bar.set(1)
    signing_process_window.update_idletasks()
    signature_string = get_sign(api_endpoint, token, request_id, signing_process_window)

    file_name = str(in_data)
    file_ending = file_name.split(".")
    file_ending = file_ending[-1]

    with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
        f.write('Request response:')
    append_new_line('{}_signature.{}'.format(in_data, file_ending),
                    "{}".format(signature_string))


def main(api_endpoint, api_key, in_data, out_data, key_name, operation, digest):

    if digest:
        signing_digest(api_endpoint, api_key, in_data, out_data, key_name, operation)
    else:
        signing(api_endpoint, api_key, in_data, out_data, key_name, operation)


def call_streaming_signing(api_endpoint, api_key, in_data, out_data, key_name, operation, digest):
    """call streaming method to pass the values from the GUI"""
    main(api_endpoint, api_key, in_data, out_data, key_name, operation, digest)
