import json
import re
import sys
import os
import shutil

DEFAULT = """{
    "DEBUG": {
        "FILE": "debug.log",
        "TIMEFORMAT": "%Y-%m-%d %H:%M:%S"
    },
    "ADDRESS": "0.0.0.0:300",
    "FRIENDLY_HOSTS": []
}
"""

def save_default(file):
    with open(file, "w") as file:
        file.write(DEFAULT)

def load_default():
    data = json.loads(DEFAULT)
    tmp = []
    
    for host in data["FRIENDLY_HOSTS"]:
        addr, port = host.split(":")
        port = int(port)
        tmp.append((addr, port))
    
    data["FRIENDLY_HOSTS"] = tmp

    addr, port = data["ADDRESS"].split(":")
    port = int(port)
    data["ADDRESS"] = (addr, port)
    
    return data

def check(data):
    if not isinstance(data, dict):
        raise ValueError 

    if not "DEBUG" in data or not isinstance(data["DEBUG"], dict):
        raise ValueError

    if not "FILE" in data["DEBUG"] or not isinstance(data["DEBUG"]["FILE"], str):
        raise ValueError

    if not "TIMEFORMAT" in data["DEBUG"] or not isinstance(data["DEBUG"]["TIMEFORMAT"], str):
        raise ValueError

    if not "FRIENDLY_HOSTS" in data or not isinstance(data["FRIENDLY_HOSTS"], list):
        raise ValueError

    tmp = []
    
    for host in data["FRIENDLY_HOSTS"]:
        if not isinstance(host, str) or not re.fullmatch(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):((6553[0-5])|(655[0-2][0-9]{1})|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([0-5]?[0-9]{1,4}))$", host):
            raise AttributeError
        addr, port = host.split(":")
        port = int(port)
        tmp.append((addr, port))
    
    data["FRIENDLY_HOSTS"] = tmp

    if not "ADDRESS" in data or not isinstance(data["ADDRESS"], str) or not re.fullmatch(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):((6553[0-5])|(655[0-2][0-9]{1})|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([0-5]?[0-9]{1,4}))$", data["ADDRESS"]):
        raise ValueError

    addr, port = data["ADDRESS"].split(":")
    port = int(port)
    data["ADDRESS"] = (addr, port)

def save_cert():
    from OpenSSL import crypto
    from socket import gethostname

    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().C = "AU"
    cert.get_subject().ST = "UNKNOWN"
    cert.get_subject().L = "UNKNOWN"
    cert.get_subject().O = "Self-signed key"
    cert.get_subject().OU = "Self-signed key"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open("certificate/cert.crt", "wb").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open("certificate/key.pem", "wb").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


def check_cert():
    if (not os.path.exists("certificate")) or os.path.isfile("certificate"):
        try:
            os.remove("certificate")
        except:
            pass
        os.mkdir("certificate")

    if (not os.path.exists("certificate/key.pem")) or os.path.isdir("certificate/key.pem") \
        or (not os.path.exists("certificate/cert.crt")) or os.path.isdir("certificate/cert.crt"):
        try:
            shutil.rmtree("certificate/key.pem")
        except:
            pass
        try:
            shutil.rmtree("certificate/cert.crt")
        except:
            pass
        
        save_cert()

def load(file = "config.json"):
    try:
        with open(file, "r") as file:
            data = json.loads(file.read())
            check(data)
    except:
        save_default(file)
        data = load_default()
    return data

file = "config.json"
if "--config" in sys.argv:
    index = sys.argv.index("--config") + 1
    if len(sys.argv) > index:
        file = sys.argv[index]
config = load(file)
check_cert()