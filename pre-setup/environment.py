#!/usr/bin/env python
from __future__ import print_function

import os
import json
import shutil
import sys

from jinja2 import Environment, FileSystemLoader

#
FILE_DIR = os.path.split(os.path.realpath(__file__))[0]
BASE_DIR = os.path.split(FILE_DIR)[0]


TEMPLATE_FILES = ['inventory', 'servers.yml']
ANSIBLE_FILES = ['ansible.cfg', 'ssh.config']
VAGRANT_FILES = ['Vagrantfile']
FILES = ANSIBLE_FILES + VAGRANT_FILES + TEMPLATE_FILES

FOLDERS = ['.vagrant']

def delete_conf(pwd):
    """
    Clean the work environment by making sure that:
        - No `Vagrant` file is present
        - If a `Vagrant` file is present, remove the VM's before deletion
        - No `.vagrant` folder is present
        - No `inventory` file is present.
    """
    files = FILES
    folders = FOLDERS

    def delete(f, func=os.remove):
        """
        Funcion to delete files or folders in `pwd`
        """
        try:
            func(f)
        except OSError as e:
            print("DELETE: " + f + ", " + e.strerror)

    for f in files:
        delete(os.path.join(pwd, f), func=os.remove)

    for f in folders:
        delete(os.path.join(pwd, f), func=shutil.rmtree)

def copy_conf(pwd):
    """
    Place configuration files to manage Ansible ssh conections.
    """
    orig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static_files')
    files = ANSIBLE_FILES + VAGRANT_FILES

    def copy(f, orig, dest):
        try:
            shutil.copy(os.path.join(orig, f), os.path.join(dest, f))
        except FileNotFoundError as e:
            print("COPY: " + f + ", " + e.strerror)

    for f in files:
        copy(f, orig, pwd)

def generate_templates(pwd):
    TEMPLATE = Environment(trim_blocks=True,
                    keep_trailing_newline=True,
                    lstrip_blocks=False,
                    loader=FileSystemLoader(os.path.join(FILE_DIR, 'templates')))

    def render_template(template_filename, context):
        return TEMPLATE.get_template(template_filename).render(context)

    def template(fname, context):
        with open(fname, 'w') as f:
            template = render_template(fname + '.j2', context)
            f.write(template)

    files = TEMPLATE_FILES
    context = json.loads(open(os.path.join(FILE_DIR, \
                                        'inventories', \
                                        'vagrant.json')).read())

    for f in files:
        template(f, context)

def main():
    print(BASE_DIR)
    delete_conf(BASE_DIR)
    copy_conf(BASE_DIR)
    generate_templates(BASE_DIR)


if __name__ == '__main__':
    main()
