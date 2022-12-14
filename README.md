# Cambridge Audio Air CLI

## About

These utilities allow you to reveal / set the radio preset settings on a
Cambridge Audio Air v2 network streamer/speaker as well as play an ad-hoc radio
station.  It might be compatible with Cambridge Audio Minx devices, though not
tested as I don't own a Minx.

## Background

My Cambridge Audio Air v2 stopped playing Classic FM.  Wireshark came to the
rescue, I noticed the device tries to play the Classic FM radio via an https
stream but the TLSv1.2 negotiation keeps failing.  Then I started inspecting
the binary control protocol between the Android "Air" app and the device.  As a
result, here are three prototyped python cli programs -
`camair-preset-dump.py`, `camair-preset-change.py` and `camair-play.py`.
Finally I was able to overwrite the preset's stream url to use a plain http
stream for Classic FM from the http url I found in
[radiofeeds](http://radiofeeds.co.uk/) 🙂

## Usage

- `camair-preset-dump.py` dumps the preset configuration as a JSON document.
- `camair-preset-change.py` changes any preset's `stream url`, `name` or the `logo url`
- `camair-play.py` plays an adhoc stream or a preset

## License

    MIT License

    Copyright (c) 2022 Attila Bogár

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
