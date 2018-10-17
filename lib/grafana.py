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
        """ A suggestion would be to encapsulate all the socket and connection logic an alternative class so testing would be easier"""
        self.connection = self.socket.socket()
        try:
            self.connection.connect(
                (
                    self.host,
                    self.port
                )
            )

            mybytes = '{name} {value} {time}\n'.format(
                name=name,
                value=value,
                time=time.time()
            )

            self.connection.send(str.encode(mybytes))
            print(name, value)
        # I would need to understand more about socket.error to not have
        # to make this more generic
        except Exception as expt:
            print("{}".format(expt))
        finally:
            self.connection.close()
