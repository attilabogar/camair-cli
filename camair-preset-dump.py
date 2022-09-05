#!/usr/bin/env python3
import socket
import struct
import sys
import argparse
import json

def getcam_preset(sock, opcode, preset):
    values = (0x00, 0x02, opcode, preset)
    packer = struct.Struct('bbbb')
    packed_data = packer.pack(*values)
    preset_data = None

    # Send data
    sock.sendall(packed_data)
    (status, xlen) = sock.recv(2)
    data = sock.recv(int(xlen))
    if data[0] == 0xff and data[1] == 0x01:
        preset_data = data[2:].decode("utf-8")
    return preset_data


def main(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, 43000)
    sock.connect(server_address)

    presets = dict({})
    for preset in range(0,10):
        name = getcam_preset(sock, 0x0a, preset)
        stream = getcam_preset(sock, 0x08, preset)
        logo = getcam_preset(sock, 0x0c, preset)
        presets[preset+1] = dict({"name": name, "stream": stream, "logo": logo})
    sock.close()
    print(json.dumps(presets, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cambridge Audio Air - Preset Dump')
    parser.add_argument('--host', metavar='host', type=str, required=True, help='Cambridge Audio Air IP Address')
    args = parser.parse_args()
    main(args.host)
