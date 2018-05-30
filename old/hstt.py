# <editor-fold desc="Working with windows certificate store">
#import wincertstore
#for storename in ("CA", "ROOT"):
#    with wincertstore.CertSystemStore(storename) as store:
#        for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
#            print(cert.get_pem())
#            print(cert.get_name())
#            print(cert.enhanced_keyusage_names())
# </editor-fold>


import urllib3
from multiprocessing.dummy import Pool as ThreadPool

urls = [
  'http://www.python1.org',
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
]

test = [2,5,7,8,]





def soma(a):
    return a+1


# make the Pool of workers
pool = ThreadPool(8)

# open the urls in their own threads
# and return the results
results = pool.map(soma, test)

# close the pool and wait for the work to finish
pool.close()
pool.join()

#for result in results:
#    print(result)

data3 = {'features_sample_folder': './features_test_data', 'server': [{'pfx_password': '', 'services': [{'service_name': 'feature', 'active': True, 'service': ':3434/Features'}, {'service_name': 'Vsu Health', 'active': True, 'service': '3434/VsuHealth'}, {'service_name': 'Vsu Health', 'active': True, 'service': '3434/DatsHealth'}], 'server_name': 'DEP1(DEV-VIRTUAL)', 'pfx_certificate': './certificates/NVOTest.pfx', 'user': 'demo', 'server': 'https://172.19.11.139', 'server_certificate': './certificates/NVOTest.pfx.cer.pem', 'sample_folder': '', 'active': True, 'password': 'demo', 'client_key': './certificates/NVOTest.pfx.key.pem'}, {'pfx_password': '', 'services': [{'service_name': 'feature', 'active': True, 'service': ':3434/Features'}, {'service_name': 'Vsu Health', 'active': True, 'service': '3434/VsuHealth'}, {'service_name': 'Vsu Health', 'active': True, 'service': '3434/DatsHealth'}], 'server_name': 'DEP3(DEV1)', 'pfx_certificate': './certificates/NVOTest.pfx', 'user': 'demo', 'server': 'https://172.18.21.5', 'server_certificate': './certificates/NVOTest.pfx.cer.pem', 'sample_folder': '', 'active': False, 'password': 'demo', 'client_key': './certificates/NVOTest.pfx.key.pem'}], 'report_folder': './report', 'health_sample_folder': './health_test_data'}



for server in data3['server']:
    if server['active']:
        print(server['server'])
        for index in range(len(server['services'])):
            print(server['services'][index]['service_name'])
