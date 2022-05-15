import base64
import PySimpleGUI as Sg
import os.path
import requests
from cbor2 import dumps, loads

end_point = "https://eu.smartkey.io/"


def generate_plain_text(plain_file, key_name):
    yield dumps({"init": {"key": {"name": key_name}, "mode": "CBC"}})
    with open(plain_file) as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            yield dumps({"plain": base64.b64encode(bytearray(data, 'utf-8'))})
            # yield dumps({"plain": data})
    yield dumps(dict(final={}))


# def encrypt(token_value: object, data: object) -> object:
#     # init streaming
#     header = {"Authorization": f"Bearer {token_value}", "Content-type": "application/cbor-seq", "Accept": "*/*"}
#     print('Started Encryption')
#     if os.path.exists(cipher_file):
#          open(cipher_file, 'w').close()
#     # generator send request in chunks
#     # refer: https://docs.python-requests.org/en/latest/user/advanced/#chunk-encoded-requests
#     # store binary response in file
#     with requests.post(f"{end_point}/crypto/v1/stream/encrypt", data= data, headers=header, stream=True) as r:
#         for data in r.iter_content(chunk_size=None):
#             for key, value in loads(data).items():
#                 if key == 'cipher':
#                     with open(cipher_file, "ab") as binary_file:
#                         # Write text or bytes to the file
#                         binary_file.write(value)
#                         # num_bytes_written = binary_file.write(value)
#                         # print("Wrote %d bytes." % num_bytes_written)

# print('Done')


def authentication(api_key):
    headers = {
        'Authorization': f"Basic {api_key}"
    }
    response = requests.post(f"{end_point}/sys/v1/session/auth", headers=headers)
    return response.json()['access_token']


def open_window(first_window_values):
    new_window_layout = [[Sg.Text("Choose a file: "), Sg.Input(), Sg.FileBrowse(key="-IN-")],
                         [Sg.T('Enter API key')], [Sg.In(k='-key1-')],
                         [Sg.T('Enter key name')], [Sg.In(k='-key2-')], [Sg.Button("Submit", key="open")]]
    second_window = Sg.Window("HSM_GUI_insert_Data", new_window_layout, modal=True, size=(800, 400))
    while True:
        event, second_window_values = second_window.read()
        if event in (None, 'Cancel'):
            break

        # print(first_window_values)
        # print(second_window_values)

        plain_file = os.path.split(second_window_values['-IN-'])
        api_key = second_window_values['-key1-']
        key_name = second_window_values['-key2-']
        plain_file = plain_file[1]

        # print(plain_file)
        # print(key_name)

        token_value = authentication(api_key)
        print(token_value)
        data = generate_plain_text(plain_file, key_name)
        print(data)
        # encrypt(token_value, data)
        second_window.close()


def main():
    layout = [[Sg.Radio('Encryption', 'num', default=True),
               Sg.Radio('Signing', 'num', default=False)],
              [Sg.Button('Submit')]]

    window = Sg.Window('HSM_GUI_choose_crypto_action', layout, size=(600, 300))

    while True:  # Event Loop
        event, first_window_values = window.Read()
        if event in (None, 'Cancel'):
            break
        # print(event, first_window_values)
        window.close()
        open_window(first_window_values)


if __name__ == "__main__":
    main()
