
import socket
import time
import boto3
from aws_composer_secret_tools.secrets import decrypt_data

class InstancePingStatus(object):

    def ssm_instance_status(self):
        """The function looks at the status of the Managed Instance."""
        iam = boto3.client('iam')
        response = iam.list_account_aliases()
        name = response['AccountAliases']
        accountname = ''.join(name)  # gets the aws account name

        ssm = boto3.client('ssm')
        paginator = ssm.get_paginator('describe_instance_information')
        page_iterator = paginator.paginate(PaginationConfig={'MaxItems': 5000})

        linuxuuid = decrypt_data("graphite.ssm.linux")
        windowsuuid = decrypt_data("graphite.ssm.windows")

        grafana = Grafana(socket)
        graphitewindowsdata = windowsuuid + accountname  # sets the folder structure for windows servers in Graphite
        graphitelinuxdata = linuxuuid + accountname  # sets the folder structure for linux servers in Graphite
        totalwindows = 0
        totallinux = 0

        for page in page_iterator:
            windowscount = 0
            linuxcount = 0

            for instance in page['InstanceInformationList']:
                instance_status = instance['PingStatus']
                server = instance['ComputerName']
                inst_id = instance['InstanceId']
                platform = instance['PlatformType']

                if instance_status == 'ConnectionLost':
                    print('platformType={}, computerName="{}", instanceID={}, pingStatus={}, '
                        'accountName={}'.format(platform,
                                                server,
                                                inst_id,
                                                instance_status,
                                                accountname))
                    if platform == 'Windows':
                        windowscount = windowscount + 1
                    elif platform == 'Linux':
                        linuxcount = linuxcount + 1

            totalwindows = totalwindows + windowscount
            totallinux = totallinux + linuxcount
        grafana.send_metric(graphitewindowsdata, totalwindows)  # sends windows data to Graphite
        grafana.send_metric(graphitelinuxdata, totallinux)  # sends linux data to Graphite

# if __name__ == "__main__":  # pragma: no cover
#     # If started from outside Lambda, this will run.
#     ssm_instance_status()