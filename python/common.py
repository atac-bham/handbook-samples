
import os

from tqdm import tqdm


def walk_packets(c10, args={}):
    """Walk a chapter 10 file based on sys.argv (type, channel, etc.)."""

    # Apply defaults.
    args['--type'] = args.get('--type') or ''
    args['--channel'] = args.get('--channel') or ''
    args['--exclude'] = args.get('--exclude') or ''

    # Parse types (if given) into ints.
    types = [t.strip() for t in args['--type'].split(',') if t.strip()]
    types = [int(t, 16) if t.startswith('0x') else int(t) for t in types]

    # Parse channel selection.
    channels = [c.strip() for c in args['--channel'].split(',') if c.strip()]
    exclude = [e.strip() for e in args['--exclude'].split(',') if e.strip()]

    for i, packet in enumerate(c10):
        if i > 0:
            if channels and str(packet.channel_id) not in channels:
                continue
            elif str(packet.channel_id) in exclude:
                continue
            elif types and packet.data_type not in types:
                continue

        yield packet


class FileProgress(tqdm):
    """Extend tqdm to show progress reading over a file based on f.tell()."""

    def __init__(self, filename, **kwargs):
        tqdm_kwargs = dict(
            dynamic_ncols=True,
            total=os.stat(filename).st_size,
            leave=False,
            unit='bytes',
            unit_scale=True)
        tqdm_kwargs.update(kwargs)
        tqdm.__init__(self, **tqdm_kwargs)
        self.last_tell = 0

    def update_from_tell(self, tell):
        self.update(tell - self.last_tell)
        self.last_tell = tell
