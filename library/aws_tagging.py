#!/usr/bin/env python

import boto3
import botocore

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
