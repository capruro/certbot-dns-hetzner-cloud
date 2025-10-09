import pytest
from unittest.mock import MagicMock, patch
from certbot_dns_hetzner_cloud.authenticator import HetznerCloudDNSAuthenticator

def test_setup_credentials_creates_client():
    # Instanz ohne __init__ der Basisklasse erstellen
    auth = object.__new__(HetznerCloudDNSAuthenticator)

    mock_credentials = MagicMock()
    mock_credentials.conf.return_value = "dummy_token"

    with patch.object(auth, "_configure_credentials", return_value=mock_credentials) as mock_configure, \
         patch("certbot_dns_hetzner_cloud.authenticator.HetznerCloudHelper", autospec=True) as mock_helper:

        auth._setup_credentials()

        mock_configure.assert_called_once_with(
            "credentials", "Hetzner Cloud INI file", {"api_token": "Hetzner Cloud API Token"}
        )
        mock_helper.assert_called_once_with("dummy_token")
        assert auth._client is mock_helper.return_value
