import os
import sys

# Allow direct execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import trim_mp3_cover_art

if __name__ == '__main__':
    trim_mp3_cover_art.main()