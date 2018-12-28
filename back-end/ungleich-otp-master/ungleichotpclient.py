import pyotp
import json
import urllib.request
import urllib.error

class UngleichOTPClient(object):
    token_name = 'token'
    name_name = 'name'
    realm_name = 'realm'

    def __init__(self, name, realm, seed, serverurl):
        self.name = name
        self.realm = realm
        self.seed = seed
        self.serverurl = serverurl

    def verify(self, name, realm, token):
        to_send = {}

        # Client credentials to be verified
        to_send['verifyname']  = name
        to_send['verifyrealm'] = realm
        to_send['verifytoken'] = token

        # Our credentials
        to_send['token'] = pyotp.TOTP(self.seed).now()
        to_send['name']  = self.name
        to_send['realm'] = self.realm

        data = json.dumps(to_send).encode("utf-8")

        req = urllib.request.Request(url=self.serverurl,
                                     data=data,
                                     headers={'Content-Type': 'application/json'},
                                     method='POST')

        f = urllib.request.urlopen(req)

        if f.status == 200:
            return True

        return False


if __name__ == '__main__':
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description='ungleichotp-client')
    parser.add_argument('-n', '--name', help="Name (for verification)", required=True)
    parser.add_argument('-r', '--realm', help="Realm (for verification)", required=True)

    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--token', help="Token (for verification)")
    g.add_argument('--seed', help="Seed (for verification)")

    args = parser.parse_args(sys.argv[1:])


    UNGLEICHOTP={}
    for env in ['UNGLEICHOTPREALM', 'UNGLEICHOTPNAME', 'UNGLEICHOTPSEED', 'UNGLEICHOTPSERVER' ]:
        if not env in os.environ:
            raise Exception("Required environment variable missing: {}".format(env))

    client = UngleichOTPClient(os.environ['UNGLEICHOTPNAME'],
                               os.environ['UNGLEICHOTPREALM'],
                               os.environ['UNGLEICHOTPSEED'],
                               os.environ['UNGLEICHOTPSERVER'])


    if args.seed:
        token = pyotp.TOTP(args.seed).now()
    else:
        token = args.token

    try:
        if client.verify(args.name, args.realm, token) == True:
            print("Verify ok")
    except urllib.error.HTTPError as e:
        print("Failed to verify: {}".format(e))
