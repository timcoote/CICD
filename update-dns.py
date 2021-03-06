# this program updates the ip address in dns for jenkins.iotaa.co.uk. The machine is identified
# as the singleton running vm tagged with the name CICD. Not finding one machine is assumed to be
# an error.  If present, AAAA records are also added.
# The code structure grabs the AWS configuration, validates in with tests, then changes the ip address

import boto3
from collections import defaultdict
import unittest2
from godaddypy import Client, Account
from godaddypy.client import BadResponse
import os
from urllib3.exceptions import HTTPError

# how long is an iterator
def count_instances (instance_collection):
    count = 0
    for x in instance_collection:
        count += 1
    return count

class TestIntegrity (unittest2.TestCase):

    def test_only_one_running_instance (self):
        self.assertEqual (count_instances (running_instances), 1, "there should be exactly one active CICD tagged host")

    def test_there_is_exactly_one_nic (self):
        for ri in running_instances:
            self.assertEqual (count_instances (ri.network_interfaces_attribute), 1, "there should be exactly one nic on the CICD host")

    @unittest2.skip ("api only allows one public ipv4 address")
    def test_there_is_exactly_one_IPv4_address (self):
        for ri in running_instances:
            self.assertEqual (len (ri.public_ip_address), 0, "there should be exactly one public IP address")


class TestGodaddy (unittest2.TestCase):
    def setUp (self):
        self.client = Client (Account (api_key=os.environ['godaddy_key'], api_secret=os.environ['godaddy_secret']))
        
# this needs fixing to read the record first, then re-add it
    @unittest2.skip ("fixme and implement")
    def test_duplicate_records_fail (self):
        # with self.assertRaises (HTTPError):
        #with self.assertRaises (Exception):
        with self.assertRaises (BadResponse):
            self.client.add_record ('iotaa.co.uk', {'data':'52.49.186.47', 'name': 'jenkins', 'ttl':600, 'type':'A'})

suite = unittest2.makeSuite (TestIntegrity)
suite.addTest (TestGodaddy ('test_duplicate_records_fail'))
#suite.addTest (TestGodaddy)


runner = unittest2.TextTestRunner()

# hosts that there should only be one of, <tagged name  of ec2 instance> : <hostname>

singletonHosts = {"CICD": "jenkins", "aos_elk": "ELK", "hubcentral": "hubcentral" }
#
class SingletonHost ():
    def __init__ (self, tagvalue):
        self.ec2 = boto3.resource('ec2')
        self.filter = [{'Name': 'tag:Name', 'Values': ['{}'.format (tagvalue)]}, {'Name': 'instance-state-name', 'Values': ['running']}]
        print ("filter, {}".format (self.filter))
## Get information for all running instances
        self.running_instances = self.ec2.instances.filter(Filters=self.filter)

    def count (self):
        return count_instances (self.running_instances)


class TestSingleHost (unittest2.TestCase):
    def setUp (self):
        self.verificationErrors = []

    def test_count (self):
        for tag, role in singletonHosts.items():
            sh = SingletonHost (tag)
            with self.subTest (sh = sh):
                print ("host: {} {}".format (tag, role))
                self.assertEqual (sh.count (), 1, "wrong number of {}".format (role))

    def tearDown (self):
        self.assertEqual ([], self.verificationErrors, "".join ([ x for x in self.verificationErrors] ))



ec2 = boto3.resource('ec2')
filter = [{'Name': 'tag:Name', 'Values': ['CICD']}, {'Name': 'instance-state-name', 'Values': ['running']}]
# Get information for all running instances
running_instances = ec2.instances.filter(Filters=filter)

suite.addTest (TestSingleHost ('test_count'))
runner.run (suite)


ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary         
    v6_addr = instance.network_interfaces_attribute[0]['Ipv6Addresses']
    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'IPv6s': v6_addr,
        'Launch Time': instance.launch_time
        }

attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time', 'IPv6s']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("------")

for x in running_instances:
  print (x.network_interfaces_attribute[0]['Ipv6Addresses'])

# values before start:
# (update) Tims-MacBook-Pro-2:godaddy tim$ python x.py 
# ['iotaa.co', 'iotaa.co.uk', 'iotaa.org']
# [{'type': 'A', 'name': '@', 'data': '139.59.135.120', 'ttl': 600}, {'type': 'A', 'name': 'demo', 'data': '192.168.43.20', 'ttl': 600}, {'type': 'A', 'name': 'hubcentral', 'data': '52.56.237.214', 'ttl': 3600}]

client = Client (Account (api_key=os.environ['godaddy_key'], api_secret=os.environ['godaddy_secret']))

print (client.get_domains ())
print (client.get_records ("iotaa.co.uk", record_type="A"))

# coote.org: temp for cert signing with letsencrypt
# print (client.update_record_ip ("87.81.133.180", "iotaa.co.uk", "demo", "A"))
# ip address handed out by hotspot on phone
# print (client.update_record_ip ("192.168.43.20", "iotaa.co.uk", "demo", "A"))
# an ec2 instance 
print (client.update_record_ip ("35.177.48.101", "iotaa.co.uk", "demo", "A"))

for ri in running_instances:
    print (client.update_record_ip ("{}".format (ri.public_ip_address), "iotaa.co.uk", "jenkins", "A"))

print (client.get_records ("iotaa.co.uk", record_type="A"))

# instant hack
#print (client.add_record ('iotaa.co.uk', {'data': '34.241.193.240', 'name': 'elk', 'ttl': 600, 'type': 'A'}))

