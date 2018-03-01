#!/usr/bin/env python3
"""
scan.py
-------

Adapted much of the code from pyinsane2's example files.
"""

import os
import time
import pathlib
import argparse

import tqdm

import pyinsane2


def setup_device(device_name=None, resolution=300, mode='Gray'):

    pyinsane2.init()

    if device_name is not None:
        device = pyinsane2.Scanner(name='brother4:net1;dev0')
    else:
        devices = pyinsane2.get_devices()
        assert (len(devices) > 0)
        device = devices[0]

    print(f"Will use: {device}")
    pyinsane2.set_scanner_opt(device, 'source', ['Auto', 'FlatBed'])
    pyinsane2.set_scanner_opt(device, 'resolution', [resolution, ])
    try:
        pyinsane2.maximize_scan_area(device)
    except Exception as exc:
        print(f"Failed to maximize scan area: {exc}")
    pyinsane2.set_scanner_opt(device, 'mode', [mode, ])

    return device


def scan(device, output_file):
    print(f"Scanning {output_file}...")
    scan_session = device.scan(multiple=False)

    expected_size = scan_session.scan.expected_size
    last_line = 0
    with tqdm.tqdm(total=expected_size[1]) as progress_bar:
        try:
            while True:
                scan_session.scan.read()
                next_line = scan_session.scan.available_lines[1]
                progress_bar.update(next_line - last_line)
                last_line = next_line
        except EOFError:
            progress_bar.update(scan_session.scan.available_lines[1] - last_line)

    img = scan_session.images[0]
    img.save(output_file, "PDF")


def main():
    parser = argparse.ArgumentParser(
        description="Scanning Program for rapid scanning with "
                    "manual switching on a flatbed.")
    parser.add_argument('dest_dir', type=str,
                        help='Directory to store scans in')
    parser.add_argument('-p', '--prefix', type=str, default='brotherscan',
                        help='Prefix for saved files.')
    parser.add_argument('-d', '--device', type=str,
                        default=None,
                        help='Name of device to use for scanning.')
    parser.add_argument('-t', '--timeout', type=int,
                        default=5,
                        help='Prefix for saved files.')
    args = parser.parse_args()

    dest_dir = pathlib.Path(os.path.expanduser(args.dest_dir)).absolute()
    dest_dir.mkdir(exist_ok=True)
    base_name = dest_dir.joinpath(args.prefix)
    device = setup_device(args.device, 300, 'Gray')

    try:
        n = 0
        while True:
            n += 1
            scan(device, f"{base_name}_{n:03d}.pdf")
            for _ in tqdm.tqdm(range(int(args.timeout / 0.1)), desc="Sleeping"):
                time.sleep(0.1)
    except (Exception, KeyboardInterrupt):
        pass
    finally:
        pyinsane2.exit()


if __name__ == "__main__":
    main()
