#!/usr/bin/python

# Copyright: (c) 2023, Rustam Mulyukov <r.muljukov@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my own modile for testing 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my own module which stores content in some file by the some path.

options:
    content:
        description: This is the content of file.
        required: true
        type: str
    path:
        description: This is the path of file
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - mulyukov.my_collection.my_own_module

author:
    - Rustam Mulyukov (@UstasNest)
'''

EXAMPLES = r'''
# Creating file on path with content
- name: Creating file
  mulyukov.my_collection.my_own_module:
    content: "hello world"
    path: "/home/vagrant/github/ansible/library/test"

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
status:
    description: Is everything is okay.
    type: bool
    returned: always
    sample: True
'''

from ansible.module_utils.basic import AnsibleModule
import os.path

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        additional_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if not os.path.exists(module.params['path']):
        f = open(module.params['path'],"w+")
        f.write(module.params['content'])
        f.close()
        result['changed'] = True
        result['message'] = 'FILE CREATED'
    else:
        f = open(module.params['path'],"r")
        data = f.read()
        f.close()
        if module.params['content'] == data:
            result['changed'] = False
            result['message'] = 'FILE EXIST'
        else:
            f = open(module.params['path'],"w")
            f.write(module.params['content'])
            f.close()            
            result['changed'] = True
            result['message'] = 'FILE CHANGED'
            result['additional_message'] = "old content: '" + data + "'"
            
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
