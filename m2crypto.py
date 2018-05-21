import M2Crypto

cert = M2Crypto.X509.load_cert('certificate.cer', M2Crypto.X509.FORMAT_DER)

pubkey = cert.get_pubkey()
pubkey.reset_context('sha256')
pubkey.verify_init()
pubkey.verify_update(content)
verified = pubkey.verify_final(signature)