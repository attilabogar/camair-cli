#!/usr/bin/env python3
import socket
import struct
import sys
import argparse

def setcam_preset(sock, opcode, preset, station_data):
    message = bytes(chr(opcode)+chr(preset-1)+station_data, 'utf-8')
    data = generic_message(sock, message)
    return len(data) == 2 and data[0] == 0xff and data[1] == 0x01

def setcam_station(sock, opcode, station_data):
    message = bytes(chr(opcode)+station_data, 'utf-8')
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

    if args.preset:
        if setcam_preset(sock, 0x0f, args.preset, ''):
            print("Play preset {:d} SUCCESSFUL".format(args.preset))
        else:
            print("Play preset {:d} FAILED".format(args.preset))
    else:
        if args.station_name:
            if setcam_station(sock, 0x15, args.station_name):
                print("Playing station name SUCCESSFUL")
            else:
                print("Playing station name FAILED")

        if args.station_stream:
            if setcam_station(sock, 0x13, args.station_stream):
                print("Setting station stream url SUCCESSFUL")
            else:
                print("Setting station stream url FAILED")

        data = generic_message(sock, b'\x1c\x50' ) # play stream
        if len(data) == 2 and data[0] == 0xff and data[1] == 0x01:
            print("Play command SUCCESSFUL")
        else:
            print("Play command FAILED")

        if args.station_logo:
            if setcam_station(sock, 0x17, args.station_logo):
                print("Setting station logo url SUCCESSFUL")
            else:
                print("Setting station logo url FAILED")

    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cambridge Audio Air')
    parser.add_argument('--host', metavar='host', type=str, required=True, help='Cambridge Audio Air IP Address')
    parser.add_argument('--preset', metavar='preset', type=int, required=False, help='Preset (1-10)')
    parser.add_argument('--station-name', metavar='name', type=str, required=False, help='Station Name')
    parser.add_argument('--station-stream', metavar='stream', type=str, required=False, help='Station Stream URL')
    parser.add_argument('--station-logo', metavar='logo', type=str, required=False, help='Station Logo URL')

    args = parser.parse_args()
    if args.preset:
        assert(args.preset>0 and args.preset<11), "Preset must be in 1..10 range"
    else:
        assert(args.station_name), "RADIO name must be defined"
        assert(args.station_stream), "RADIO stream-url must be defined"
    main(args)
