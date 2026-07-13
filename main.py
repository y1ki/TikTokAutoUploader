import sys
import os

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from src.core.app import Application

if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
