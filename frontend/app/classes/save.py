#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import re
import shutil
from datetime import datetime

import psutil
from flask import jsonify, send_file


class Save():

    def __init__(self):
        self.mount_point = ""
        return None

    def usb_check(self) -> dict:
        """Check if a USB storage device is connected or not.

        Returns:
            dict: contains the connection status.
        """
        self.mount_point = ""
        usb_devices = []

        # Check mounted disk partitions
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts or 'usb' in partition.device:
                # Consider the device a USB or removable if it contains 'removable' or 'usb'
                self.mount_point = partition.mountpoint
                usb_devices.append(partition.device)
                return jsonify({"status": True,
                                "message": "USB storage connected",
                                "mount_point": self.mount_point})

        # If no USB devices were found
        return jsonify({"status": False,
                        "message": "USB storage not connected"})

    def save_capture(self, token, method) -> any:
        """Save the capture to the USB device or push a ZIP
        file to download.

        Args:
            token (str): capture token
            method (str): method used to save

        Returns:
            dict: operation status OR Flask answer.
        """
        if re.match(r"[A-F0-9]{8}", token):
            try:
                cd = datetime.now().strftime("%d%m%Y-%H%M")
                if method == "usb" and self.mount_point:
                    archive_path = "{}/SpyGuard_{}".format(self.mount_point, cd)
                    if shutil.make_archive(archive_path, "zip", "/tmp/{}/".format(token)):
                        shutil.rmtree("/tmp/{}/".format(token))
                        return jsonify({"status": True,
                                        "message": "Capture saved on the USB key"})

                elif method == "url":
                    archive_path = "/tmp/SpyGuard_{}".format(cd)
                    if shutil.make_archive(archive_path, "zip", "/tmp/{}/".format(token)):
                        shutil.rmtree("/tmp/{}/".format(token))
                        with open("{}.zip".format(archive_path), "rb") as f:
                            return send_file(
                                io.BytesIO(f.read()),
                                mimetype="application/octet-stream",
                                as_attachment=True,
                                attachment_filename="SpyGuard_{}.zip".format(cd))
            except Exception as e:
                return jsonify({"status": False,
                                "message": "Error while saving capture: {}".format(str(e))})
        else:
            return jsonify({"status": False,
                            "message": "Bad token value"})
