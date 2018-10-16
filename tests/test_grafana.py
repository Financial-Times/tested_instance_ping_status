from lib.grafana import Grafana
import pytest
from pytest_mock import mocker
from io import StringIO
import sys
from .FakeSocket import FakeSocket

@pytest.fixture
def mock_socket(mocker):
    socket = mocker.MagicMock()
    return socket

@pytest.fixture
def grafana(mock_socket):
    return Grafana(mock_socket)

def test_it_stores_default_port_and_host(grafana):
    assert(grafana.host =='graphitev2.ft.com' )
    assert(grafana.port == 2003)

def test_it_creates_a_new_socket_object(grafana):
    grafana.send_metric("some_metric", 1)
    assert(grafana.socket.socket.called)

def test_it_opens_a_connection(grafana):
    grafana.send_metric("some_metric", 1)
    grafana.connection.connect.assert_called_with((grafana.host, grafana.port))

def test_it_sends_encoded_metric_data_to_connection(grafana, mocker):
    mocker.patch('time.time',return_value='1539720884.111624')
    grafana.send_metric("some_metric", 1)
    grafana.connection.send.assert_called_with(b'some_metric 1 1539720884.111624\n')

def test_it_prints_name_and_value_log(grafana, mocker):
    out = StringIO()
    sys.stdout = out
    mocker.patch('time.time',return_value='1539720884.111624')
    grafana.send_metric("some_metric", 1)
    output = out.getvalue().strip()
    assert(output == "some_metric 1")

def test_it_closes_connection_after_sending_metric(grafana):
    grafana.send_metric("some_metric", 1)
    assert(grafana.connection.close.called)

def test_it_logs_error_when_socket_error_raised(grafana):
    grafana = Grafana(FakeSocket)
    out = StringIO()
    sys.stdout = out
    grafana.send_metric("some_metric", 1)
    output = out.getvalue().strip()
    assert(output == "Something went wrong bad connection")
    












