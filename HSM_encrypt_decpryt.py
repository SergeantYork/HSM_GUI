#!/usr/bin/env python3
import asyncio
import io
import time
import platform
import aiofiles
import aiohttp
import aioitertools
import cbor2

my_os = platform.system()
if my_os == 'linux':
    import uvloop

BLOCK_SIZE = 511 * 1024


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
                with open('kid_iv.txt', 'w') as f:
                    f.write('Your KID and IV for later decryption:')
                append_new_line('kid_iv.txt', 'kid:{}'.format(init["kid"]))
                append_new_line('kid_iv.txt', 'iv:{}'.format(init["iv"].hex()))
            elif "cipher" in item:
                await cipher_out.write(item["cipher"])
            elif "final" in item:
                end = time.time()
                print("Processed in ! {:.2f} seconds".format(end - start))
                break
            elif "error" in item:
                print("received error frame: {}".format(item["error"]))
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
    check_os = platform.system()

    if check_os == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if check_os == 'linux':
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    asyncio.run(main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv))