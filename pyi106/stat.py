#!/usr/bin/env python

"""
  stat.py - Display some basic information about the channels within a
    Chapter 10 file.

 Copyright (c) 2015 Micah Ferrill

 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are
 met:

   * Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

   * Neither the name Irig106.org nor the names of its contributors may
     be used to endorse or promote products derived from this software
     without specific prior written permission.

 This software is provided by the copyright holders and contributors
 "as is" and any express or implied warranties, including, but not
 limited to, the implied warranties of merchantability and fitness for
 a particular purpose are disclaimed. In no event shall the copyright
 owner or contributors be liable for any direct, indirect, incidental,
 special, exemplary, or consequential damages (including, but not
 limited to, procurement of substitute goods or services; loss of use,
 data, or profits; or business interruption) however caused and on any
 theory of liability, whether in contract, strict liability, or tort
 (including negligence or otherwise) arising in any way out of the use
 of this software, even if advised of the possibility of such damage.
"""

__doc__ = """usage: stat.py <file> [options]

Options:
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include(csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE                 The types of data to show (csv, may \
be decimal or hex eg: 0x40)."""

from contextlib import closing

from docopt import docopt
from Py106.Packet import IO, FileMode, Status, DataType

from walk import walk_packets


if __name__ == '__main__':

    # Get commandline args.
    args = docopt(__doc__)

    channels, packets, size = ([], 0, 0)

    # Open the source file.
    with closing(IO()) as PktIO:
        RetStatus = PktIO.open(args['<file>'], FileMode.READ)
        if RetStatus != Status.OK:
            print "Error opening data file %s" % args['<file>']
            raise SystemExit

        # Iterate over selected packets (based on args).
        for packet in walk_packets(PktIO.packet_headers(), args):

            # Increment overall size and packet count.
            size += packet.PacketLen
            packets += 1

            # Find the channel info based on ID and type.
            channel_index = None
            for i, channel in enumerate(channels):
                if channel['id'] == packet.ChID and \
                        channel['type'] == packet.DataType:
                    channel_index = i
                    break

            # Find the channel info based on ID and type.
            if channel_index is None:
                channel_index = len(channels)
                channels.append({'packets': 0,
                                 'type': packet.DataType,
                                 'id': packet.ChID})

            # Increment the counter.
            channels[channel_index]['packets'] += 1

    # Print details for each channel.
    print('Channel ID     Data Type' + 'Packets'.rjust(46))
    print('-' * 80)
    for channel in channels:
        dtype = DataType.name(channel['type'])
        print (''.join((('Channel %s' % channel['id']).ljust(15),
                       ('%s - %s' % (hex(channel['type']), dtype)).ljust(35),
                       ('%s packets' % channel['packets']).rjust(20))))

    # Find a more readable size unit than bytes.
    units = ['gb', 'mb', 'kb']
    unit = 'b'
    while size > 1024 and units:
        size /= 1024.0
        unit = units.pop()

    # Print file summary.
    print('-' * 80)
    print('Summary for %s:' % args['<file>'])
    print('    Size: %s %s' % (round(size, 2), unit))
    print('    Packets: %s' % packets)
    print('    Channels: %s' % len(channels))
