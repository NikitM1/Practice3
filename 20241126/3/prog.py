import sys;import struct
try:
    data = sys.stdin.buffer.read(44)
    if len(data)< 44: raise BaseException
    else: 
        riff, size, wave, fmt, fmt_size, audio_format, channels, rate, _, _, bits, data, data_size = struct.unpack('<4sI4s4sIHHIIHH4sI', data)    
        if riff != b'RIFF' or wave != b'WAVE' or fmt != b'fmt ' or data != b'data': raise BaseException 
        print(f"Size={size}, Type={audio_format}, Channels={channels}, Rate={rate}, Bits={bits}, Data size={data_size}")
except: print('NO')