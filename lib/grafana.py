# import socket
import time
class Grafana(object):
    """A wrapper to make it nice and simple to send data to the FT's graphite instance."""

    def __init__(
            self,
            socket_class,
            host='graphitev2.ft.com',
            port=2003
            
    ):
        """Default Graphite connection details."""
        self.host = host
        self.port = port
        self.socket = socket_class

    def send_metric(self, name, value):
        """Use this method to send a value to a certain address in graphite."""
        connection = self.socket.socket()
        # try:
        #     connection.connect(
        #         (
        #             self.host,
        #             self.port
        #         )
        #     )

        #     mybytes = '{name} {value} {time}\n'.format(
        #         name=name,
        #         value=value,
        #         time=time.time()
        #     )

        #     connection.send(str.encode(mybytes))
        #     print(name, value)
        # except socket.error as expt:
        #     print("{}".format(expt))
        # finally:
        #     connection.close()
