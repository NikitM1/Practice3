import sys
import struct

try:
    file_data = sys.stdin.buffer.read()
    if len(file_data) < 44:
        print("NO")
    else:
        try:
            (
                riff_header,
                file_length,
                wave_format,
                fmt_chunk,
                fmt_length,
                audio_fmt,
                channel_count,
                sample_rate,
                _,
                _,
                bit_depth,
                data_chunk,
                data_length,
            ) = struct.unpack("<4sI4s4sIHHIIHH4sI", file_data[:44])
        except struct.error:
            print("NO")
        else:
            if (
                riff_header != b"RIFF"
                or wave_format != b"WAVE"
                or fmt_chunk != b"fmt "
                or data_chunk != b"data"
            ):
                print("NO")
            else:
                print(
                    f"Size={file_length}, Type={audio_fmt}, Channels={channel_count}, Rate={sample_rate}, Bits={bit_depth}, Data size={data_length}"
                )
except Exception:
    print("NO")
