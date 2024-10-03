import os
import subprocess as sp
import netifaces as ni
import requests
import re
import qrcode
import base64
import random
import platform
from io import BytesIO
from pywifi import const, PyWiFi, Profile
from app.utils import read_config

class Network(object):
    def __init__(self):
        self.AP_SSID = False
        self.AP_PASS = False
        self.iface_out = read_config(("network", "out"))
        self.iface_in = read_config(("network", "in"))
        self.random_choice_alphabet = "abcdef1234567890"

    def check_status(self) -> dict:
        """Check network status"""
        ctx = {"internet": self.check_internet()}

        for iface in ni.interfaces():
            if iface != self.iface_in and iface.startswith(("wl", "en", "et", "ww")):
                addrs = ni.ifaddresses(iface)
                try:
                    ctx["ip_out"] = addrs[ni.AF_INET][0]["addr"]
                except:
                    ctx["ip_out"] = "Not connected"
        return ctx

    def wifi_list_networks(self) -> dict:
        """List available Wi-Fi networks"""
        if platform.system() == 'Windows':
            return self.wifi_list_windows()
        else:
            return self.wifi_list_linux()

    def wifi_list_windows(self) -> dict:
        """Use pywifi to list available Wi-Fi networks on Windows"""
        wifi = PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        scan_results = iface.scan_results()

        networks = []
        for network in scan_results:
            networks.append({
                "name": network.ssid,
                "signal": network.signal
            })
        return {"networks": networks}

    def wifi_list_linux(self) -> dict:
        """Use nmcli to list available Wi-Fi networks on Linux"""
        networks = []
        if self.iface_out.startswith("wl"):
            sh = sp.Popen(["nmcli", "-f", "SSID,SIGNAL", "dev", "wifi", "list", "ifname", self.iface_out], stdout=sp.PIPE, stderr=sp.PIPE)
            sh = sh.communicate()

            for network in [n.decode("utf8") for n in sh[0].splitlines()][1:]:
                name = network.strip()[:-3].strip()
                signal = network.strip()[-3:].strip()
                if name not in [n["name"] for n in networks] and name != "--":
                    networks.append({"name": name, "signal": int(signal)})
        return {"networks": networks}

    def wifi_setup(self, ssid, password) -> dict:
        """Connect to a Wi-Fi network"""
        if platform.system() == 'Windows':
            return self.wifi_setup_windows(ssid, password)
        else:
            return self.wifi_setup_linux(ssid, password)

    def wifi_setup_windows(self, ssid, password) -> dict:
        """Connect to a Wi-Fi network using pywifi on Windows"""
        wifi = PyWiFi()
        iface = wifi.interfaces()[0]

        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()
        iface.add_network_profile(profile)
        iface.connect(iface.add_network_profile(profile))

        return {"status": True, "message": "Wi-Fi connected"}

    def wifi_setup_linux(self, ssid, password) -> dict:
        """Use nmcli to connect to a Wi-Fi network on Linux"""
        if len(password) >= 8 and len(ssid):
            sh = sp.Popen(["nmcli", "dev", "wifi", "connect", ssid, "password", password, "ifname", self.iface_out], stdout=sp.PIPE, stderr=sp.PIPE)
            sh = sh.communicate()

            if re.match(".*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}.*", sh[0].decode('utf8')):
                return {"status": True, "message": "Wi-Fi connected"}
            else:
                return {"status": False, "message": "Wi-Fi not connected"}
        else:
            return {"status": False, "message": "Empty SSID or password length less than 8 chars."}

    def start_hotspot(self) -> dict:
        """Start an access point (AP)"""
        if platform.system() == 'Windows':
            return {"status": False, "message": "Hotspot feature is not available on Windows"}
        else:
            return self.start_hotspot_linux()

    def start_hotspot_linux(self) -> dict:
        """Start an access point using nmcli on Linux"""
        self.delete_hotspot()
        try:
            if read_config(("network", "tokenized_ssids")):
                token = "".join([random.choice(self.random_choice_alphabet) for i in range(4)])
                self.AP_SSID = random.choice(read_config(("network", "ssids"))) + "-" + token
            else:
                self.AP_SSID = random.choice(read_config(("network", "ssids")))

        except:
            token = "".join([random.choice(self.random_choice_alphabet) for i in range(4)])
            self.AP_SSID = "wifi-" + token

        self.AP_PASS = "".join([random.choice(self.random_choice_alphabet) for i in range(8)])

        sp.Popen(["nmcli", "con", "add", "type", "wifi", "ifname", self.iface_in, "con-name", self.AP_SSID, "autoconnect", "yes", "ssid", self.AP_SSID]).wait()
        sp.Popen(["nmcli", "con", "modify", self.AP_SSID, "802-11-wireless.mode", "ap", "802-11-wireless.band", "bg", "ipv4.method", "shared"]).wait()
        sp.Popen(["nmcli", "con", "modify", self.AP_SSID, "wifi-sec.key-mgmt", "wpa-psk", "wifi-sec.psk", self.AP_PASS]).wait()

        if self.launch_hotstop():
            return {"status": True, "message": "AP started", "ssid": self.AP_SSID, "password": self.AP_PASS, "qrcode": self.generate_qr_code()}
        else:
            return {"status": False, "message": "Error while creating AP."}

    def generate_qr_code(self) -> str:
        """Generate a QR code based on SSID and password."""
        qrc = qrcode.make("WIFI:S:{};T:WPA;P:{};;".format(self.AP_SSID, self.AP_PASS))
        buffered = BytesIO()
        qrc.save(buffered, format="PNG")
        return "data:image/png;base64,{}".format(base64.b64encode(buffered.getvalue()).decode("utf8"))

    def check_internet(self) -> bool:
        """Check internet connectivity"""
        try:
            url = read_config(("network", "internet_check"))
            requests.get(url, timeout=10)
            return True
        except:
            return False
