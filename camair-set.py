#!/usr/bin/env python3
import socket
import struct
import sys
import argparse

def setcam(sock, opcode, preset, preset_data):
    bs = bytes(preset_data, 'utf-8')
    values = (0x00, len(bs)+2, opcode, preset-1, bs)
    packer = struct.Struct('bbbb%ds' % (len(bs),))
    packed_data = packer.pack(*values)
    sock.sendall(packed_data)
    (status, xlen) = sock.recv(2)
    data = sock.recv(int(xlen))
    if data[0] == 0xff and data[1] == 0x01:
        return True
    return False


def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (args.host, 43000)
    sock.connect(server_address)

    if args.set_name:
        if setcam(sock, 0x0b, args.preset, args.set_name):
            print("Setting preset {:d} name SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} name FAILED".format(args.preset))

    if args.set_stream:
        if setcam(sock, 0x09, args.preset, args.set_stream):
            print("Setting preset {:d} stream url SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} stream url FAILED".format(args.preset))

    if args.set_logo:
        if setcam(sock, 0x0d, args.preset, args.set_logo):
            print("Setting preset {:d} logo url SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} logo url FAILED".format(args.preset))

    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cambridge Audio Air')
    parser.add_argument('--host', metavar='host', type=str, required=True, help='Cambridge Audio Air IP address')
    parser.add_argument('--preset', metavar='preset', type=int, required=True, help='Preset (1-10)')
    parser.add_argument('--set-name', metavar='name', type=str, required=False, help='Station Name')
    parser.add_argument('--set-stream', metavar='stream', type=str, required=False, help='Station Name')
    parser.add_argument('--set-logo', metavar='logo', type=str, required=False, help='Station Name')
    args = parser.parse_args()
    assert(args.preset>0 and args.preset<11), "Preset must be in 1..10 range"
    main(args)
