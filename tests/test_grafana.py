from lib.grafana import Grafana
import pytest
from pytest_mock import mocker

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

def test_it_opens_a_connection(grafana,mocker):
    mocker.patch('socket.socket')
    grafana.send_metric("some_metric", 1)
    socket.socket.assert_called_once()



