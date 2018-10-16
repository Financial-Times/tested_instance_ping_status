import socket
# from python_version_verifier import python_3_6_handler

@python_3_6_handler
def lambda_handler(event, context):  # pylint: disable=unused-argument
    """If started from Lambda, this will run."""
    ssm_instance_status()