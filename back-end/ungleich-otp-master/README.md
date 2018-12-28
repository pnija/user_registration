# ungleichotp #

ungleich-otp is a full blown authentication and authorisation service
made for micro services.

The basic idea is that every micro service has a (long term) triple
constisting of (name, realm, seed) and creates time based tokens.

This basically revamps Kerberos in a simple way into the web area.

ungleichotp has been created and is maintained by [ungleich](https://ungleich.ch/).

Related documentation:

* [Python pyotp](https://pyotp.readthedocs.io/)
* [RFC6238, TOTP](https://tools.ietf.org/html/rfc6238)
* [RFC4120, Kerberos](https://tools.ietf.org/html/rfc4120)

## Overview ##

This repository contains...

* ungleichotpserver: the reference implementation of the ungleichotp server
* ungleichotpclient.py: a sample implementation of an ungleichotp client


## Verifying a token using ungleichotpclient.py ##

Assuming you want to verify
(name=ipv6only, realm=ungleich-intern, token=498593) is a
valid triple and you do have credentials to access ungleich-otp
(name=info@ungleich.ch, realm=ungleich-admin, seed=PZKBPTHDGSLZBKIZ),
then the following call will verify the token:

```
UNGLEICHOTPNAME=info@ungleich.ch \
UNGLEICHOTPREALM=ungleich-admin \
UNGLEICHOTPSEED=PZKBPTHDGSLZBKIZ \
UNGLEICHOTPSERVER=http://localhost:8000/ungleichotp/verify/ \
    python ungleichotpclient.py -n  -r ungleich --token 498593
```

You can also veriy using a seed:

```
UNGLEICHOTPNAME=info@ungleich.ch \
UNGLEICHOTPREALM=ungleich-admin \
UNGLEICHOTPSEED=PZKBPTHDGSLZBKIZ \
UNGLEICHOTPSERVER=http://localhost:8000/ungleichotp/verify/ \
    python ungleichotpclient.py -n  -r ungleich --seed CEKXVG3235PO2HDW
```

The client requires pyotp.

## Server Setup instructions ##

This is a standard django project and thus can be easily setup using

```
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py runserver
```


## Realms ##

Access is granting/denied based on realms. There are two reserved
realms, all other realms can be used by the users:

### Reserved realms

Conceptually the realms "ungleich-admin" and "ungleich-auth" are
reserved for higher priviliged applications.

Usually there is only 1 entry in ungleich-admin that is used to
bootstrap and manage ungleich-otp.

All micro services that are trusted to authenticate another micro
service should have an entry in the ungleich-auth realm, which allows
them to verify a token of somebody else.


| Name             | Capabilities                               |
|------------------+--------------------------------------------|
| ungleich-admin   | authenticate, create, delete, list, update |
| ungleich-auth    | authenticate                               |
| all other realms | NO ACCESS                                  |



## Verify using http POST  ##

Post a JSON object to the server at /ungleichotp/verify/ that
contains the following elements:

Request JSON object:

```
{
    name: "your-name",
    realm: "your-realm",
    token: "current time based token",
    verifyname: "name that wants to be authenticated",
    verifyrealm: "realm that wants to be authenticated",
    verifytoken: "token that wants to be authenticated",
}
```

Response JSON object:

Either HTTP 200 with
```
{
    status: "OK",
}
```

OR return code 403:

* If token for authenticating is wrong, you get

```
{"detail":"Incorrect authentication credentials."}
```

* If token that is being verified is wrong, you get

```
{"detail":"You do not have permission to perform this action."}
```

## Authorize the request ##

From the ungleichotp-server, you get a validated information that a
name on a realm authenticated successfully. The associated permissions
("authorization") is application specific and needs to be decided by
your application.


## Limitations ##

* Name, Realm and seed are hard coded to 128 bytes length. This can be
  changed, if necessary.
* Only python3 support for ungleichotp


## TODOs

- [x] (server) Serialize / input request
- [x] (server) Make seed read only
- [x] (server) Implement registering of new entries
- [x] (server) OTPSerializer: allow to read seed for admin
- [x] (server) Implement deleting entry
- [x] (server) Include verify in ModelSerializer
- [x] (server) Map name+realm == User (?)
  - name == name@realm
  - password is used for admin login (?)
  - seed
  - custom auth method
- [n] (server) Try to fake username for django based on name+realm (?)
  - No need
- [n] (server) maybe overwrite get_username()
  - No need
- [x] (server) Use Custom authentication  - needs to have a user!
- [x] (server) Implement creating new "User" by POST / Model based
- [n] (server) Remove hard coded JSON in /verify (no - good enough for the moment)
- [x] (server) Fully rename server from ungleichotp to ungleichotpserver
- [ ] (security) Ensure that only the right realms can verify
- [ ] (security) Ensure that only the right realms can manage
- [ ] (doc) Add proper documentation
- [ ] (server) Add tests for verify
- [ ] (server) Add tests for authentication
- [ ] (server) move totp constants into settings
- [ ] (server) move field lengths into settings
- [ ] (server) Document how admin vs. rest works
- [ ] (server, client) Make settings adjustable by environment - k8s/docker compatible
- [ ] (server, client) Read DB from outside (?) (fallback to sqlite)
- [x] (client) Establish auth using urllib
- [ ] (client) Bootstrap Django + DRF (including an object for CRUD)
- [ ] (client) Add custom authentication / remote auth
- [ ] (client) Show case: any realm vs. specific realm
- [ ] (library) Write a "client library" that can use ungleichotp
- [ ] (library) extract generic parts from server
- [ ] (library) upload to pypi



## Changelog

### 0.6, 2018-11-18

* Reuse TokenSerializer for VerifySerializer logic

### 0.5, 2018-11-18

* Require authentication on all rest endpoints by token
