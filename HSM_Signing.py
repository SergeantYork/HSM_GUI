#!/usr/bin/python

from __future__ import print_function

import argparse
import base64
import os
import sys
import sdkms

import sdkms.v1

from sdkms.v1.models.cipher_mode import CipherMode
from sdkms.v1.models.object_type import ObjectType
from sdkms.v1.models.digest_algorithm import DigestAlgorithm
from sdkms.v1.models.elliptic_curve import EllipticCurve

api_instances = {}
ca_certificate = None
cl_args = None


def print_debug(*args, **kwargs):
    if cl_args.debug:
        print(*args, **kwargs)


def get_api_instance(name):
    return api_instances[name]


def parse_arguments(api_endpoint , api_key):
    parser = argparse.ArgumentParser(description='SDKMS API perf/stress test')

    # This construction allows us to use the API endpoint if it's specified
    # on the command-line, then use the environment variable if it's set,
    # then use the program-default endpoint if neither is set.

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
        print('Please specify an API key via the --api-key option or '
              'FORTANIX_API_KEY')
        print('environment variable')
        exit(1)

    global ca_certificate
    if cl_args.ca_certificate:
        ca_certificate = cl_args.ca_certificate


def initialize_api_clients():
    # TODO: We should have a separate auth endpoint for API keys, so we
    # don't need to do this parsing in the client code.

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


def turn_to_byte_array(in_data):
    text_file = open(in_data, "r")
    data = text_file.read()
    text_file.close()
    encoded_data = data.encode()
    data_byte_array = bytearray(encoded_data)
    return data_byte_array


def signing(in_data, key_name):
    data = turn_to_byte_array(in_data)
    digest_request = sdkms.v1.DigestRequest(alg=DigestAlgorithm.SHA256, data=data)
    digest = get_api_instance('digest').compute_digest(digest_request).digest
    print(".......SHA2-Digest Generation")
    key_name = "b4224df8-e564-458f-ab78-5503a93b9fef"  #For RSA only
    sign_request = sdkms.v1.SignRequest(hash_alg=DigestAlgorithm.SHA256, hash=digest)
    sign_result = get_api_instance('signverify').sign(key_name, sign_request)
    print(".......SHA2-Signing")
    verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA256, hash=digest,
                                            signature=sign_result.signature)
    verify_result = get_api_instance('signverify').verify(key_name, verify_request)
    assert verify_result.result, "SHA2-Signature verification didn't succeed!"
    print(".......SHA2-Verification")


def main(api_endpoint, api_key, in_data, out_data, key_name, operation):
    ObjectType.RSA
    parse_arguments(api_endpoint, api_key)
    initialize_api_clients()
    signing(in_data, key_name)


def call_streaming_signing(api_endpoint, api_key, in_data, out_data, key_name, operation):
    main(api_endpoint, api_key, in_data, out_data, key_name, operation)
