from pathlib import Path
from models import Post

import argparse
import datetime
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', choices=('yes', 'no'), help='Upload')
    args = parser.parse_args()

    if(args.upload == 'yes'):
        print('Uploading')

    current = Post('md5', 'date', 'title', 'body')