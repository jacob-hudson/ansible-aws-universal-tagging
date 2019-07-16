#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import ec2_argument_spec, get_aws_connection_info
import requests, json
import sys
import boto3
import botocore

def add_tags(resource, tags):

    client = boto3.client('resourcegroupstaggingapi')

    for tag in tags:
        response = client.tag_resources(
            ResourceARNList=[
            resource,
            ],
            Tags=tag
        )

    return response


def tagging(params):
    role = False
    resource = params["resource"]
    tags = params["tags"]
    region = params["region"]

    result = add_tags(resource, tags)

    return False, True, result

def main():

    fields = {
        "role": {"required": False, "type": "str"},
        "resource": {"required": True, "type": "str"},
        "tags": {"required": True, "type": "list"},
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