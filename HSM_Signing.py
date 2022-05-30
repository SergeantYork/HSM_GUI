#!/usr/bin/python
from __future__ import print_function
import argparse
import base64
import os
import hashlib
import sdkms

import sdkms.v1

from sdkms.v1.models.digest_algorithm import DigestAlgorithm

api_instances = {}
ca_certificate = None
cl_args = None


# TODO: create a digest screen

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


def print_debug(*args, **kwargs):
    if cl_args.debug:
        print(*args, **kwargs)


def get_api_instance(name):
    return api_instances[name]


def parse_arguments(api_endpoint, api_key):
    parser = argparse.ArgumentParser(description='SDKMS API perf/stress test')

    """This construction allows us to use the API endpoint if it's specified
       on the command-line, then use the environment variable if it's set,
       then use the program-default endpoint if neither is set"""

    parser.add_argument('--api-endpoint',
                        default=os.getenv('FORTANIX_API_ENDPOINT',
                                          api_endpoint))

    parser.add_argument('--api-key',
                        default=os.getenv('FORTANIX_API_KEY', None))

    parser.add_argument('--debug', default=False, action='store_true',
                        help='enable debug logging')

    parser.add_argument('--no-verify-ssl', default=True, action='store_false',
                        dest='verify_ssl',
                        help='Disables SSL verification. Useful for '
                             'locally running SDKMS')

    parser.add_argument('--ca-certificate', help='Set the CA certificate to be'
                                                 'used for the TLS root of trust')

    global cl_args
    cl_args = parser.parse_args()
    cl_args.api_key = api_key

    if cl_args.api_key is None:
        print('No API key specified.')
        print('Please specify an API key')
        print('environment variable')
        exit(1)

    global ca_certificate
    if cl_args.ca_certificate:
        ca_certificate = cl_args.ca_certificate


def initialize_api_clients():
    # Start the session using the API key
    api_key = base64.b64decode(cl_args.api_key).decode('ascii')
    print_debug('Using API key {}'.format(api_key))
    parts = api_key.split(':')
    if len(parts) != 2:
        print('Invalid API key provided')
        exit(1)

    config = sdkms.v1.configuration.Configuration()
    config.username = parts[0]
    config.password = parts[1]
    config.debug = cl_args.debug

    if ca_certificate:
        config.ssl_ca_cert = ca_certificate

    print_debug('API key components: {} {}'.format(config.username,
                                                   config.password))

    config.verify_ssl = cl_args.verify_ssl

    print_debug('Using API endpoint {}'.format(cl_args.api_endpoint))
    config.host = cl_args.api_endpoint

    client = sdkms.v1.ApiClient(configuration=config)

    client.configuration.debug = True

    auth_instance = sdkms.v1.AuthenticationApi(api_client=client)
    auth = auth_instance.authorize()
    print_debug(auth)

    # The swagger interface calls this type of authorization an 'apiKey'.
    # This is not related to the SDKMS notion of an API key. The swagger
    # apiKey is our auth token.

    config.api_key['Authorization'] = auth.access_token
    config.api_key_prefix['Authorization'] = 'Bearer'

    api_instances['auth'] = auth_instance
    api_instances['sobjects'] = sdkms.v1.SecurityObjectsApi(
        api_client=client)
    api_instances['crypto'] = sdkms.v1.EncryptionAndDecryptionApi(
        api_client=client)
    api_instances['signverify'] = sdkms.v1.SignAndVerifyApi(
        api_client=client)
    api_instances['digest'] = sdkms.v1.DigestApi(api_client=client)
    api_instances['sobjects'] = sdkms.v1.SecurityObjectsApi(
        api_client=client)


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


def get_key_id(name):
    """This function turns key name e.g "RSA_Test" and return the UUID"""
    api_key = get_api_instance('sobjects').get_security_objects(name=name)[0]
    return api_key.kid


def signing(in_data, key_name, operation):
    """This is a signing function using the regular functionality no API streaming digest is done on the computer
       and sent to the SaaS HSM for signing"""

    print("signing:{}".format(operation))
    # "SHA2-256", "SHA3-256"
    key_uuid = get_key_id(key_name)

    if operation == 'SHA3-256':
        result = hash_file(in_data, operation)

        result_digest = bytearray(result)

        print("my digest:{}".format(result_digest))

        print(".......SHA3-Digest Generation")
        sign_request = sdkms.v1.SignRequest(hash_alg=DigestAlgorithm.SHA3_256, hash=result_digest)
        sign_result = get_api_instance('signverify').sign(key_uuid, sign_request)

        hash_sign_string = str(sign_result.signature)
        signature = hash_sign_string.split("bytearray")
        signature = signature[-1]
        file_name = str(in_data)
        file_ending = file_name.split(".")
        file_ending = file_ending[-1]

        with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
            f.write('Hash signature:')
        append_new_line('{}_signature.{}'.format(in_data, file_ending), signature)

        print(".......SHA3-Signing")
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA3_256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA3-Signature verification didn't succeed!"
        print(".......SHA3-Verification")

    if operation == 'SHA2-256':
        result = hash_file(in_data, operation)

        result_digest = bytearray(result)

        print("my digest:{}".format(result_digest))
        print(".......SHA2-Digest Generation")

        sign_request = sdkms.v1.SignRequest(hash_alg=DigestAlgorithm.SHA256, hash=result_digest)
        sign_result = get_api_instance('signverify').sign(key_uuid, sign_request)

        hash_sign_string = str(sign_result.signature)
        signature = hash_sign_string.split("bytearray")
        signature = signature[-1]
        file_ending = str(in_data)
        file_ending = file_ending.split(".")
        file_ending = file_ending[-1]

        with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
            f.write('Hash signature:')

        append_new_line('{}_signature.{}'.format(in_data, file_ending), signature)

        print(".......SHA2-Signing")
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA2-Signature verification didn't succeed!"
        print(".......SHA2-Verification")


def signing_digest(in_data, key_name, operation):
    """This is a signing function using the regular functionality no API streaming digest is done on the computer
       and sent to the SaaS HSM for signing"""

    print("signing:{}".format(operation))
    # "SHA2-256", "SHA3-256"
    key_uuid = get_key_id(key_name)

    if operation == 'SHA3-256':
        fh = open("{}".format(in_data), 'rb')
        result_digest = bytearray(fh.read)

        print("my digest:{}".format(result_digest))

        sign_request = sdkms.v1.SignRequest(hash_alg=DigestAlgorithm.SHA3_256, hash=result_digest)
        sign_result = get_api_instance('signverify').sign(key_uuid, sign_request)

        hash_sign_string = str(sign_result.signature)
        signature = hash_sign_string.split("bytearray")
        signature = signature[-1]
        file_name = str(in_data)
        file_ending = file_name.split(".")
        file_ending = file_ending[-1]

        with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
            f.write('Hash signature:')
        append_new_line('{}_signature.{}'.format(in_data, file_ending), signature)

        print(".......SHA3-Signing")
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA3_256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA3-Signature verification didn't succeed!"
        print(".......SHA3-Verification")

    if operation == 'SHA2-256':
        fh = open("{}".format(in_data), 'rb')
        result_digest = bytearray(fh.read)
        print("my digest:{}".format(result_digest))

        sign_request = sdkms.v1.SignRequest(hash_alg=DigestAlgorithm.SHA256, hash=result_digest)
        sign_result = get_api_instance('signverify').sign(key_uuid, sign_request)

        hash_sign_string = str(sign_result.signature)
        signature = hash_sign_string.split("bytearray")
        signature = signature[-1]
        file_ending = str(in_data)
        file_ending = file_ending.split(".")
        file_ending = file_ending[-1]

        with open('{}_signature.{}'.format(in_data, file_ending), 'w') as f:
            f.write('Hash signature:')

        append_new_line('{}_signature.{}'.format(in_data, file_ending), signature)

        print(".......SHA2-Signing")
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA2-Signature verification didn't succeed!"
        print(".......SHA2-Verification")


def main(api_endpoint, api_key, in_data, out_data, key_name, operation, digest):
    parse_arguments(api_endpoint, api_key)
    initialize_api_clients()
    if digest:
        signing_digest(in_data, key_name, operation)
    else:
        signing(in_data, key_name, operation)


def call_streaming_signing(api_endpoint, api_key, in_data, out_data, key_name, operation, digest):
    """call streaming method to pass the values from the GUI"""
    main(api_endpoint, api_key, in_data, out_data, key_name, operation, digest)
