import json
import pyotp
import urllib.request
import urllib.parse

serverurl="http://localhost:8000/ungleichotp/verify/"
totp=pyotp.TOTP("PZKBPTHDGSLZBKIZ")

to_send={}
to_send['name'] = "info@ungleich.ch"
to_send['verifyname'] = to_send['name']

to_send['token'] = totp.now()
to_send['verifytoken'] = to_send['token']

to_send['realm'] = "ungleich-admin"
to_send['verifyrealm'] = to_send['realm']

data = json.dumps(to_send)
print(data)

with open("outdata", "w") as fd:
    fd.write(data)
    fd.write("\n")


# Post to test server!
#data = urllib.parse.urlencode(bytes(data, encoding="utf-8"))
#data = urllib.parse.urlencode(to_send)
#data = bytes(data, encoding="utf-8")
data = data.encode("utf-8")

print(data)

req = urllib.request.Request(url=serverurl, data=data, headers={'Content-Type': 'application/json'}, method='POST')

print(req)

with urllib.request.urlopen(req) as f:
    print(f.status)

    if f.status == 200:
        print("all good")
    print(f.reason)
    print(f.getcode())
