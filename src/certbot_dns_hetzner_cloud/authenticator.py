import tldextract
from certbot.plugins import dns_common
from datetime import datetime, timezone
from certbot_dns_hetzner_cloud.hetzner_cloud_helper import HetznerCloudHelper

def split_validation_name(validation_name: str) -> tuple[str, str]:
    extract = tldextract.extract(validation_name)
    zone_name = extract.top_domain_under_public_suffix
    record_name = validation_name[:-len(zone_name) - 1].rstrip(".")
    return zone_name, record_name


class HetznerCloudDNSAuthenticator(dns_common.DNSAuthenticator):
    """Authenticator for DNS-01 challenges using Hetzner Cloud DNS"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hetzner_dns_helper: HetznerCloudHelper | None = None

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=30):
        super().add_parser_arguments(add, default_propagation_seconds)

    @classmethod
    def more_info(cls) -> str:
        return "Plugin for handling DNS-01 challenges via Hetzner Cloud DNS API."

    def _setup_credentials(self) -> None:
        credentials = self._configure_credentials("credentials", "Hetzner Cloud INI file", {
            "api_token": "Hetzner Cloud API Token"
        })
        api_token = credentials.conf("api_token")
        self._client = HetznerCloudHelper(api_token)

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        zone_name, record_name = split_validation_name(validation_name)
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.hetzner_dns_helper.put_txt_record(
            zone=zone_name,
            name=record_name,
            value=validation,
            comment=f"created by hetzner cloud plugin at {timestamp}"
        )

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        zone_name, record_name = split_validation_name(validation_name)
        self.hetzner_dns_helper.delete_txt_record(
            zone=zone_name,
            name=record_name
        )
