"""
    Looks up public-facing IPs in AWS and optionally performs
    a Shodan search against them.
"""

import os
import boto3
import shodan as sd
import click

def get_public_ips():
    """ Gets all external IPs in a AWS account """

    client = boto3.client('ec2', region_name='us-east-1')
    res = client.describe_network_interfaces()
    enis = res['NetworkInterfaces']
    instance_enis = []
    other_enis = []
    all_public_ips = []

    for eni in enis:
        if 'Attachment' and 'Association' in eni:
            all_public_ips.append(eni['Association']['PublicIp'])
            if 'InstanceId' in eni['Attachment']:
                instance_enis.append(eni)
            else:
                other_enis.append(eni)

    if instance_enis:
        print "Instances:"
        for instance in instance_enis:
            print "%s:\t%s" % (instance['Association']['PublicIp'],
                               instance['Attachment']['InstanceId'])


    if other_enis:
        print "\nOther ENIs:"
        for other_eni in other_enis:
            print "%s:\t%s" % (other_eni['Association']['PublicIp'], other_eni['Description'])

    return all_public_ips


def shodan_search_host(api, ip_addr):
    """ Searches for the host in Shodan """
    try:
        host = api.host(ip_addr)
        print "IP: %s" % host['ip_str']
        for item in host['data']:
            print """  Port: %s, Banner: %s""" % (item['port'], item['data'])
    except sd.exception.APIError, ex:
        print "%s:\t%s" % (ip_addr, ex)

#pylint: disable=no-value-for-parameter
@click.command()
@click.option('-s', '--shodan', is_flag=True, help='Performs Shodan host seach on each IP found')
def main(shodan):
    """ Entrypoint """
    public_ips = get_public_ips()
    if shodan:
        try:
            shodan_api_key = os.environ["SHODAN_API_KEY"]
        except KeyError:
            print("Please set your Shodan API key in the environment variable SHODAN_API_KEY")
            exit(1)
        print "\nPerforming Shodan Search..."
        api = sd.Shodan(shodan_api_key)
        for ip_addr in public_ips:
            shodan_search_host(api, ip_addr)

main()
