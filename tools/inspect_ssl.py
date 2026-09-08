import ssl
import sys
print('ssl module:', ssl)
print('ssl file:', getattr(ssl, '__file__', 'built-in'))
print('has wrap_socket:', hasattr(ssl, 'wrap_socket'))
print('attrs:', sorted([n for n in dir(ssl) if 'wrap' in n or 'PROTOCOL' in n]))
print('version:', sys.version)
