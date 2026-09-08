"""Minimal opuslib stub to avoid requiring native libopus for text-only usage.

Expose a lightweight, no-op `Encoder` and common symbols so third-party
libraries that import `opuslib` can proceed without native DLLs.
"""
from . import api as api

# Backwards-friendly aliases expected by various wrappers
Encoder = api.OpusEncoder
opus_encoder_create = api.opus_encoder_create
opus_encoder_destroy = api.opus_encoder_destroy
opus_encoder_ctl = api.opus_encoder_ctl
opus_encoder_get_size = api.opus_encoder_get_size
Decoder = api.OpusDecoder
opus_decoder_create = api.opus_decoder_create
opus_decoder_destroy = api.opus_decoder_destroy
opus_decode = api.opus_decode

__all__ = [
	'api', 'Encoder', 'Decoder',
	'opus_encoder_create', 'opus_encoder_destroy',
	'opus_encoder_ctl', 'opus_encoder_get_size',
	'opus_decoder_create', 'opus_decoder_destroy', 'opus_decode'
]
