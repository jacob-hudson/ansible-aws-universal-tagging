#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import ec2_argument_spec, get_aws_connection_info
import requests, json
import sys
import boto3
import botocore

def tag_ec2():

    resource = "i-03ba8b4dde20e9a66"

    client = boto3.client('ec2')

    response = client.create_tags(
    DryRun=False,
    Resources=[
    resource,
    ],
    Tags=[
    {
        'Key': 'ansible_test',
        'Value': 'new_ansible_moudle'
        },
    ] 
    )


def tagging(params):
    role = False
    resource = params["resource"]
    tags = params["tags"]
    region = params["region"]

    return False, True, json.dumps(tags)

def main():

    fields = {
        "role": {"required": False, "type": "str"},
        "resource": {"required": True, "type": "str"},
        "tags": {"required": True, "type": "str"},
        "region": {"required": False, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = tagging(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)


if __name__ == "__main__":
    main()