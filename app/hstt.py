import wincertstore
for storename in ("CA", "ROOT"):
    with wincertstore.CertSystemStore(storename) as store:
        for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
            print(cert.get_pem())
            print(cert.get_name())
            print(cert.enhanced_keyusage_names())