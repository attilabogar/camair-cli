#!/usr/bin/env python3
import socket
import struct
import sys
import argparse

def setcam_preset(sock, opcode, preset, preset_data):
    message = bytes(chr(opcode)+chr(preset-1)+station_data, 'utf-8')
    data = generic_message(sock, message)
    return len(data) == 2 and data[0] == 0xff and data[1] == 0x01

def generic_message(sock, message):
    values = (0x00, len(message), message)
    packer = struct.Struct('bb%ds' % (len(message),))
    packed_data = packer.pack(*values)
    sock.sendall(packed_data)
    status = 0x00
    while status == 0x00:
        status = sock.recv(1)[0]
    data = sock.recv(status)
    return data


def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (args.host, 43000)
    sock.connect(server_address)

    if args.set_name:
        if setcam_preset(sock, 0x0b, args.preset, args.set_name):
            print("Setting preset {:d} name SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} name FAILED".format(args.preset))

    if args.set_stream:
        if setcam_preset(sock, 0x09, args.preset, args.set_stream):
            print("Setting preset {:d} stream url SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} stream url FAILED".format(args.preset))

    if args.set_logo:
        if setcam_preset(sock, 0x0d, args.preset, args.set_logo):
            print("Setting preset {:d} logo url SUCCESSFUL".format(args.preset))
        else:
            print("Setting preset {:d} logo url FAILED".format(args.preset))

    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cambridge Audio Air')
    parser.add_argument('--host', metavar='host', type=str, required=True, help='Cambridge Audio Air IP Address')
    parser.add_argument('--preset', metavar='preset', type=int, required=True, help='Preset (1-10)')
    parser.add_argument('--set-name', metavar='name', type=str, required=False, help='Station Name')
    parser.add_argument('--set-stream', metavar='stream', type=str, required=False, help='Station Stream URL')
    parser.add_argument('--set-logo', metavar='logo', type=str, required=False, help='Station Logo URL')
    args = parser.parse_args()
    assert(args.preset>0 and args.preset<11), "Preset must be in 1..10 range"
    main(args)
