#!/usr/bin/env python3
import asyncio
import io
import os
import platform
import time
import aiofiles
import aiohttp
import aioitertools
import cbor2
import progressbar

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


async def encrypt(plain_in, cipher_out, key_name, bearer, client, api_endpoint, file_name):
    file_stat = os.stat(file_name)
    iteration_value = (file_stat.st_size / BLOCK_SIZE)
    bar = progressbar.ProgressBar(maxval=iteration_value,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ',
                                           progressbar.Percentage()])
    print()
    bar.start()

    i = 0
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

            if item != "final":
                if i < (iteration_value - 1):
                    i = i + 1
                bar.update(i)

                # add progress bar here
            if "init" in item:
                init = item["init"]
                with open('{}_kid_iv.txt'.format(file_name), 'w') as f:
                    f.write('Your KID and IV for later decryption:')

                append_new_line('{}_kid_iv.txt'.format(file_name), 'key_name:{}'.format(key_name))
                append_new_line('{}_kid_iv.txt'.format(file_name), 'kid:{}'.format(init["kid"]))
                append_new_line('{}_kid_iv.txt'.format(file_name), 'iv:{}'.format(init["iv"].hex()))

            elif "cipher" in item:
                await cipher_out.write(item["cipher"])

            elif "final" in item:
                end = time.time()
                bar.finish()
                print("Processed in ! {:.2f} seconds".format(end - start))
                print("kid: {}, iv: {}".format(init["kid"], init["iv"].hex()))
                print(".....encryption finished....")
                break

            elif "error" in item:
                print("received error frame: {}".format(item["error"]))
                break


async def decrypt(cipher_in, plain_out, key_name, bearer, client, api_endpoint, file_name, iv):
    start = time.time()
    file_stat = os.stat(file_name)
    iteration_value = (file_stat.st_size / BLOCK_SIZE)
    bar = progressbar.ProgressBar(maxval=iteration_value, widgets=[progressbar.Bar('=', '[', ']'), ' ',
                                                                   progressbar.Percentage()])
    bar.start()
    print()
    i = 0
    plain_chunks = chunk_input_file(cipher_in)
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
            print()
            print("HTTP error: {}: {}".format(response.status, await response.text()))
            return

        # for demonstration; in real impl improve error handling
        response_items = decode_cbor_stream(response.content.iter_any())
        async for item in response_items:

            if item != "final":
                if i < (iteration_value - 1):
                    i = i + 1
                    bar.update(i)
                    print()

            if "init" in item:
                init = item["init"]
            elif "plain" in item:
                await plain_out.write(item["plain"])
            elif "final" in item:
                end = time.time()
                bar.finish()
                print()
                print("Process in {:.2f} seconds".format(end - start))
                print(".....decryption finished....")

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


async def main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv, file_name):
    time_out = aiohttp.ClientTimeout(total=10000)
    async with aiohttp.ClientSession(timeout=time_out) as client:
        auth = await get_auth(client, api_endpoint, api_key)
        async with aiofiles.open(in_data, "rb") as in_data:

            async with aiofiles.open(out_data, "wb") as out_data:
                if operation == "encrypt":
                    print(".....encryption started....")
                    print()
                    await encrypt(in_data, out_data, key_name, auth, client, api_endpoint, file_name)
                if operation == "decrypt":
                    print(".....decryption started....")
                    await decrypt(in_data, out_data, key_name, auth, client, api_endpoint, file_name, iv)


def call_streaming_encrypt_decrypt(api_endpoint, api_key, in_data, out_data, key_name, operation, iv=None):
    check_os = platform.system()

    if check_os == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if check_os == 'linux':
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    file_name = str(in_data)
    asyncio.run(main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv, file_name))
