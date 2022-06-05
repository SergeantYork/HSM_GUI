def signing(in_data, key_name, operation):
    """This is a signing function using the regular functionality no API streaming digest is done on the computer
       and sent to the SaaS HSM for signing"""
    print("signing:{}".format(operation))
    signing_process_window = SigningProgressWindow()

    # "SHA2-256", "SHA3-256"
    key_uuid = get_key_id(key_name)

    if operation == 'SHA3-256':
        result = hash_file(in_data, operation)

        result_digest = bytearray(result)
        signing_process_window.terminal_output.configure(text="SHA2-signing process started",
                                                         font=("Roboto", 10, "bold"))
        signing_process_window.progress_bar.set(0)
        signing_process_window.update_idletasks()
        sleep(2)
        print("my digest:{}".format(result_digest))
        print("SHA3-Digest Generation")

        signing_process_window.terminal_output.configure(text="SHA2-Digest Generation",
                                                         font=("Roboto", 10, "bold"))
        signing_process_window.progress_bar.set(0.33)
        signing_process_window.update_idletasks()
        sleep(2)

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

        signing_process_window.terminal_output.configure(text=".......SHA3-Signing",
                                                         font=("Roboto", 10, "bold"))
        print(".......SHA3-Signing")
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA3_256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA3-Signature verification didn't succeed!"
        print(".......SHA3-Verification")

        signing_process_window.progress_bar.set(1)
        signing_process_window.update_idletasks()

        if verify_result.result:
            signing_process_window.terminal_output.configure(text="Signature verified",
                                                             font=("Roboto", 10, "bold"))
            sleep(2)
            signing_process_window.terminal_output.configure(text="Signature process Ended",
                                                             font=("Roboto", 10, "bold"))
        else:
            signing_process_window.terminal_output.configure(text="Signature verification failed",
                                                             font=("Roboto", 10, "bold"))
    if operation == 'SHA2-256':
        result = hash_file(in_data, operation)

        result_digest = bytearray(result)
        signing_process_window.progress_bar.set(0)
        signing_process_window.update_idletasks()
        signing_process_window.terminal_output.configure(text="SHA2-signing process started",
                                                         font=("Roboto", 10, "bold"))
        sleep(2)
        print("my digest:{}".format(result_digest))
        print(".......SHA2-Digest Generation")
        signing_process_window.terminal_output.configure(text="SHA2-Digest Generation",
                                                         font=("Roboto", 10, "bold"))
        signing_process_window.progress_bar.set(0.33)
        signing_process_window.update_idletasks()
        sleep(2)

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
        signing_process_window.terminal_output.configure(text="SHA2-Signing",
                                                         font=("Roboto", 10, "bold"))
        print(".......SHA2-Signing")
        signing_process_window.progress_bar.set(0.66)
        signing_process_window.update_idletasks()
        sleep(2)
        verify_request = sdkms.v1.VerifyRequest(hash_alg=DigestAlgorithm.SHA256, hash=result_digest,
                                                signature=sign_result.signature)

        verify_result = get_api_instance('signverify').verify(key_uuid, verify_request)
        assert verify_result.result, "SHA2-Signature verification didn't succeed!"

        print(".......SHA2-Verification")
        signing_process_window.progress_bar.set(1)
        signing_process_window.update_idletasks()

        if verify_result.result:
            signing_process_window.terminal_output.configure(text="Signature verified",
                                                             font=("Roboto", 10, "bold"))
            sleep(2)
            signing_process_window.terminal_output.configure(text="Signature process Ended",
                                                             font=("Roboto", 10, "bold"))
        else:
            signing_process_window.terminal_output.configure(text="Signature verification failed",
                                                             font=("Roboto", 10, "bold"))