#!/usr/bin/env python

import sys
import os
import subprocess
import glob
import shutil
from jinja2 import Template

def render(id_pub):
    id_pub = os.path.basename(id_pub)
    with open('Dockerfile.template') as input, \
         open('Dockerfile', 'w') as output:
        template = Template(input.read())
        output.write(template.render(id_pub=id_pub))

def build(tag):
    subprocess.call('docker build -t {} .'.format(tag).split())
                     
def find_id_pub():
    ids = glob.glob(os.path.expanduser('~/.ssh/id_*.pub'))
    return os.path.abspath(ids[0])

def get_id_pub(id_pub):
    shutil.copy(id_pub, '.')
    
def main(tag=None):
    try:
        id_pub = find_id_pub()
        get_id_pub(id_pub)
        render(id_pub)
        tag = tag or 'autobuild'
        build(tag)
    except IndexError:
        print("Couldn't find public key for ssh")

if __name__ == '__main__':
    try:
        tag = sys.argv[1]
    except IndexError:
        tag = None
    main(tag)
