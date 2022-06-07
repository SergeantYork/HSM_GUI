#!/usr/bin/env python3
import asyncio
import platform
import string
import time
import aiofiles
import aiohttp
import aioitertools
import cbor2
import os
import io

from my_encryption_decryption_process_window import ProgressWindow

my_os = platform.system()
if my_os == 'Linux':
    import uvloop

BLOCK_SIZE = 511 * 1024
PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1000
HEIGHT = 700


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
    progress_window = ProgressWindow()
    file_stat = os.stat(file_name)
    number_of_iterations = (file_stat.st_size / BLOCK_SIZE)
    i = 0
    progress_window.progress_bar.set(0)
    progress_window.update_idletasks()
    progress_window.terminal_output.configure(text="Encryption started",
                                              font=("Roboto", 10, "bold"))
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
            print("HTTP error: {}".format(await response.text()))
            progress_window.terminal_output.configure(text="HTTP error:{} please check log file"
                                                      .format(await response.text()),
                                                      font=("Roboto", 10, "bold"))
            return

        # for demonstration; in real impl improve error handling
        response_items = decode_cbor_stream(response.content.iter_any())
        async for item in response_items:

            if item != "final":
                if i < (number_of_iterations - 1):
                    i = i + 1
                progress_bar_update = (i / number_of_iterations)
                progress_window.progress_bar.set(progress_bar_update)
                progress_window.update_idletasks()

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
                progress_window.progress_bar.set(1)
                print("Processed in ! {:.2f} seconds".format(end - start))
                print(".....encryption finished....")
                progress_window.terminal_output.configure(text="Processed in ! {:.2f} seconds\n"
                                                               "Encryption finished".format(end - start),
                                                          font=("Roboto", 10, "bold"))
                break

            elif "error" in item:
                print("received error frame: {}".format(item["error"]))
                progress_window.terminal_output.configure(text="received error frame: {}".format(item["error"]))
                break
    log_file_path = PATH + "/log_file.txt"
    if my_os == 'linux':
        cmd = 'cat > {}'.format(log_file_path)
        os.system(cmd)


async def decrypt(cipher_in, plain_out, key_name, bearer, client, api_endpoint, file_name, iv):
    start = time.time()
    progress_window = ProgressWindow()
    file_stat = os.stat(file_name)
    number_of_iterations = (file_stat.st_size / BLOCK_SIZE)
    i = 0
    progress_window.progress_bar.set(0)
    progress_window.update_idletasks()
    progress_window.terminal_output.configure(text="Decryption started",
                                              font=("Roboto", 10, "bold"))
    plain_chunks = chunk_input_file(cipher_in)
    print("decryption started")
    error = all(c in string.hexdigits for c in iv)
    if not error:
        progress_window.terminal_output.configure(text="IV is not right please close session and check log file")

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
            print("HTTP error: {}".format(await response.text()))
            progress_window.terminal_output.configure(text="HTTP error:{}".format(await response.text()),
                                                      font=("Roboto", 10, "bold"))
            return

        # for demonstration; in real impl improve error handling
        response_items = decode_cbor_stream(response.content.iter_any())
        async for item in response_items:

            if item != "final":
                if i < (number_of_iterations - 1):
                    i = i + 1
                progress_bar_update = (i / number_of_iterations)
                progress_window.progress_bar.set(progress_bar_update)
                progress_window.update_idletasks()

            if "plain" in item:
                await plain_out.write(item["plain"])

            elif "final" in item:
                end = time.time()
                progress_window.progress_bar.set(1)
                print("Process in {:.2f} seconds".format(end - start))
                print(".....decryption finished....")
                progress_window.terminal_output.configure(text="Processed in ! {:.2f} seconds\n"
                                                               "Decryption finished".format(end - start),
                                                          font=("Roboto", 10, "bold"))
                break
            elif "error" in item:
                progress_window.terminal_output.configure(text="received error frame: {}".format(item["error"]))
                print("received error frame: {}".format(item["error"]))
                break

    log_file_path = PATH + "/log_file.txt"
    if my_os == 'linux':
        cmd = 'cat > {}'.format(log_file_path)
        os.system(cmd)


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
        response_status = response.status
        if response_status == 401:
            progress_window = ProgressWindow()
            progress_window.progress_bar.set(0)
            progress_window.update_idletasks()
            progress_window.terminal_output.configure(text="Wrong API key please close session and check log file",
                                                      font=("Roboto", 10, "bold"))
        body = await response.json()
        return body["access_token"]


async def main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv, file_name):
    time_out = aiohttp.ClientTimeout(total=10000)
    async with aiohttp.ClientSession(timeout=time_out) as client:
        auth = await get_auth(client, api_endpoint, api_key)
        async with aiofiles.open(in_data, "rb") as in_data:

            async with aiofiles.open(out_data, "wb") as out_data:
                if operation == "encrypt":
                    await encrypt(in_data, out_data, key_name, auth, client, api_endpoint, file_name)
                if operation == "decrypt":
                    await decrypt(in_data, out_data, key_name, auth, client, api_endpoint, file_name, iv)


def call_streaming_encrypt_decrypt(api_endpoint, api_key, in_data, out_data, key_name, operation, iv=None):
    check_os = platform.system()

    if check_os == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if check_os == 'linux':
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    file_name = str(in_data)
    asyncio.run(main(api_endpoint, api_key, in_data, out_data, key_name, operation, iv, file_name))
