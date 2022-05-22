#!/usr/bin/env python3

import asyncio
import aiofiles
import aiohttp
import aioitertools
import cbor2
import io
import sys
import time
import pathlib
import os

BLOCK_SIZE = 511 * 1024


async def encrypt(plain_in, cipher_out, key_name, bearer, client, api_endpoint):
    start = time.time()
    plain_chunks = chunk_input_file(plain_in)
    request_items = aioitertools.chain(
        ({"init": {"key": {"name": key_name}, "mode": "CBC"}},),
        ({"plain": bytes(chunk)} async for chunk in plain_chunks),
        ({"final": {}},))
    request_bytes = (cbor2.dumps(item) async for item in request_items)

    async with client.post("{}/crypto/v1/stream/encrypt".format(api_endpoint),
                           headers={"Authorization": "Bearer {}".format(bearer)},
                           data=request_bytes
                           ) as response:
        if response.status != 200:
            print("HTTP error: {}: {}".format(response.status, await response.text()))
            return

        # for demonstration; in real impl improve error handling
        response_items = decode_cbor_stream(response.content.iter_any())
        async for item in response_items:

            if "init" in item:
                init = item["init"]
                print("kid: {}, iv: {}".format(init["kid"], init["iv"].hex()))
            elif "cipher" in item:
                await cipher_out.write(item["cipher"])
            elif "final" in item:
                end = time.time()
                print("Processed in ! {:.2f} seconds".format(end - start))
                break
            elif "error" in item:
                print("recieved error frame: {}".format(item["error"]))
                break


async def decrypt(plain_in, cipher_out, key_name, bearer, client, iv, api_endpoint):
    start = time.time()
    plain_chunks = chunk_input_file(plain_in)
    request_items = aioitertools.chain(
        ({"init": {"key": {"name": key_name}, "mode": "CBC", "iv": bytes.fromhex(iv)}},),
        ({"cipher": bytes(chunk)} async for chunk in plain_chunks),
        ({"final": {}},))
    request_bytes = (cbor2.dumps(item) async for item in request_items)

    async with client.post("{}/crypto/v1/stream/decrypt".format(api_endpoint),
                           headers={"Authorization": "Bearer {}".format(bearer)},
                           data=request_bytes
                           ) as response:
        if response.status != 200:
            print("HTTP error: {}: {}".format(response.status, await response.text()))
            return

        # for demonstration; in real impl improve error handling
        response_items = decode_cbor_stream(response.content.iter_any())
        async for item in response_items:
            # print(item)
            if "init" in item:
                init = item["init"]
                print("kid: {}".format(init["kid"]))
            elif "plain" in item:
                await cipher_out.write(item["plain"])
            elif "final" in item:
                end = time.time()
                print("Process in {:.2f}".format(end - start))
                break
            elif "error" in item:
                print("received error frame: {}".format(item["error"]))
                break


async def chunk_input_file(file):
    while True:
        chunk = await file.read(BLOCK_SIZE)
        if chunk == b'':
            break
        yield chunk


async def decode_cbor_stream(chunks):
    buf = io.BytesIO()
    async for chunk in chunks:
        buf.write(chunk)
        buf.seek(0)
        try:
            while True:
                pos = buf.tell()
                item = cbor2.load(buf)
                yield item
        except cbor2.CBORDecodeEOF:
            remainder = buf.getvalue()[pos:]
            buf.seek(0)
            buf.write(remainder)
            buf.truncate()
    if buf.tell() != 0:
        raise cbor2.CBORDecodeEOF("unexpected EOF while decoding CBOR sequence")


async def get_auth(client, api_endpoint, api_key):
    async with client.post("{}/sys/v1/session/auth".format(api_endpoint),
                           headers={"Authorization": "Basic {}".format(api_key)}
                           ) as response:
        body = await response.json()
        return body["access_token"]


async def main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv):
    async with aiohttp.ClientSession() as client:
        auth = await get_auth(client, api_endpoint, api_key)
        async with aiofiles.open(in_data, "rb") as in_data:
            async with aiofiles.open(out_data, "wb") as out_data:
                if operation == "encrypt":
                    await encrypt(in_data, out_data, key_name, auth, client, api_endpoint)
                if operation == "decrypt":
                    await decrypt(in_data, out_data, key_name, auth, client, iv, api_endpoint)


def call_streaming_encrypt_decrypt(api_endpoint, api_key, in_data, out_data, key_name, operation, iv=None):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv))
