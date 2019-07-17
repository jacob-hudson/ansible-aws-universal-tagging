#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import ec2_argument_spec, get_aws_connection_info
import requests, json
import sys
import boto3
import botocore

def add_tags(resource, tags):

    client = boto3.client('resourcegroupstaggingapi')

    response = client.tag_resources(
        ResourceARNList=[
        resource,
        ],
        Tags=tags
    )

    return response

def generate_arn(resource, region):
    # get account ID
    iam = boto3.resource('iam')
    account_id = iam.CurrentUser().arn.split(':')[4]

    if resource.startswith("i-"):
        complete_arn = "arn:aws:ec2:" + region + ":" + account_id + ":instance/" + resource
    elif resource.startswith("vol-"):
        complete_arn = "arn:aws:ec2:" + region + ":" + account_id + ":volume/" + resource
    elif resource.startswith("snap-"):
        complete_arn = "arn:aws:ec2:" + region + ":" + account_id + ":volume/" + resource
    else:
        complete_arn = "arn:aws:s3:::" + resource

    return complete_arn

def tagging(params):
    role = False
    resource = params["resource"]
    tags = params["tags"]
    region = params["region"]

    # build complete ARN for EC2 Instances, Snapshots, and EBS Volumes
    if not resource.startswith("awn:aws"):
        resource = generate_arn(resource, region)
    result = add_tags(resource, tags)

    if int(result['ResponseMetadata']['HTTPStatusCode']) > 400:
        return True, True, result
    else:
        return False, True, result

def main():

    fields = {
        "resource": {"required": True, "type": "str"},
        "tags": {"required": True, "type": "dict"},
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