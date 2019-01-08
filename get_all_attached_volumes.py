#!/usr/bin/python

import boto3

MY_AWS_ID = '904298664928'
#MY_AWS_ID = '644376117491'

#REGION = 'eu-west-1'
REGION = 'eu-west-2'
FORMAT_STRING = "%-28s\t%-20s\t%-9s\t%-21s\t%-4s\t%-8s\t%s"
#manual_instance_ids = ["i-00664e81036710a1b"]

def get_instance_ids(owner, region):
  responses = []
  instances = []
  instance_ids = []
  tags = []
  instance_names = []

  client = boto3.client('ec2', region)
  for response in client.describe_instances(Filters=[{'Name': 'owner-id', 'Values': [owner]}])['Reservations']:
    responses.append(response)
  for reservation in responses:
    instances.append(reservation['Instances'])
  for instance in instances:
    instance_ids.append(instance[0]['InstanceId'])
    tags.append(instance[0]['Tags'])
  for tag in tags:
    for x in tag:
      for key,val in x.items():
        if val == "Name":
           instance_names.append(x['Value'])

  return instance_ids, instance_names

def get_instance_attr(owner, region, inst_ids, inst_names):
  list_all_attr = []
  client = boto3.client('ec2', region)

  i = 0
  for instance in inst_ids:
  #for instance in manual_instance_ids:
    for block in client.describe_instance_attribute(InstanceId=instance, Attribute='blockDeviceMapping')['BlockDeviceMappings']:
      volume_id = block['Ebs']['VolumeId']
      for vol_attr in client.describe_volumes(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Volumes']:
        string = FORMAT_STRING % (inst_names[i], instance, block['DeviceName'], block['Ebs']['VolumeId'], vol_attr['Size'], vol_attr['VolumeType'], block['Ebs']['DeleteOnTermination'])
        list_all_attr.append(string)
    i +=1

  return list_all_attr


def format_attr(attrs):
  title = FORMAT_STRING % ("Instance Name","Instance ID","Device","Volume ID","Size","Type","Delete On Termination")
  print title
  attrs.sort()
  for attr in attrs:
    print attr

def main():
  ids, names = get_instance_ids(MY_AWS_ID, REGION)
  attributes = get_instance_attr(MY_AWS_ID, REGION, ids, names)
  format_attr(attributes)

if __name__ == "__main__":
  main()
