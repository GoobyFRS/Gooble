"""Stub of opuslib.api to prevent native DLL loading when audio is not used.
This provides minimal symbols used by higher-level libraries so imports succeed.
"""

# Common constants
OPUS_OK = 0
OPUS_BAD_ARG = -1

# Basic stub functions return safe dummy objects or values.

def opus_encoder_create(*args, **kwargs):
    return OpusEncoder(*args, **kwargs)

def opus_encoder_destroy(encoder, *args, **kwargs):
    try:
        encoder.destroy()
    except Exception:
        pass
    return None

def opus_encoder_ctl(*args, **kwargs):
    # No-op control
    return 0

def opus_encoder_get_size(*args, **kwargs):
    return 1

# Provide an object-like API used by wrappers. Methods are no-ops that
# raise only if audio functions are actually attempted.
class OpusEncoder:
    def __init__(self, *args, **kwargs):
        self._closed = False

    def encode(self, pcm_data, frame_size):
        raise RuntimeError("Opus audio disabled: encode not supported in stub")

    def destroy(self):
        self._closed = True

    def get_size(self):
        return 1

# Decoder stubs
def opus_decoder_create(*args, **kwargs):
    return OpusDecoder(*args, **kwargs)

def opus_decoder_destroy(decoder, *args, **kwargs):
    try:
        decoder.destroy()
    except Exception:
        pass
    return None

def opus_decode(decoder, data, frame_size, decode_fec=False):
    raise RuntimeError("Opus audio disabled: decode not supported in stub")


class OpusDecoder:
    def __init__(self, *args, **kwargs):
        self._closed = False

    def decode(self, data, frame_size, decode_fec=False):
        raise RuntimeError("Opus audio disabled: decode not supported in stub")

    def destroy(self):
        self._closed = True

# expose a simple API mapping
__all__ = [
    'OPUS_OK', 'OPUS_BAD_ARG',
    'opus_encoder_create', 'opus_encoder_destroy', 'opus_encoder_ctl', 'opus_encoder_get_size',
    'OpusEncoder',
    'opus_decoder_create', 'opus_decoder_destroy', 'opus_decode', 'OpusDecoder'
]
