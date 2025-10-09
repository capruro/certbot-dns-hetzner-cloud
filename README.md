# Certbot DNS Plugin for Hetzner Cloud DNS
This is a Certbot DNS plugin for the new Hetzner Cloud DNS, which allows you to automate the process of obtaining and 
renewing SSL/TLS certificates using the DNS-01 challenge method. This Plugin is not compatible with the old Hetzner DNS 
Console and you might want to take a look at the [certbot-dns-hetzner][1] plugin instead.

## Setup
### Installation
To install the Certbot DNS plugin for Hetzner Cloud DNS, you can either use `pip` or `snap`.

#### Installation using *pip*
If you installed Certbot within a virtual environment (e.g., `/opt/certbot`) as per [official Certbot instructions][2] 
you can install the plugin using the following command:
```bash
/opt/certbot/bin/pip install certbot-dns-hetzner-cloud
```

#### Installation using *snap*
If you installed Certbot using `snap`, you can install the plugin with the following command:
```bash
sudo snap install certbot-dns-hetzner-cloud
```
#### Verification

After installation, you can verify that the plugin is available by running:
```bash
certbot plugins
```

you should see `dns-hetzner-cloud` listed among the available plugins.

### Storing the API Token
Create a configuration file under `/etc/letsencrypt/hetzner_cloud.ini` with the following content:
```ini
# Hetzner Cloud API Token
dns_hetzner_cloud_api_token = your_api_token_here
```

Make sure to set the correct permissions for the configuration file to protect your API token:
```bash
sudo chmod 600 /etc/letsencrypt/hetzner_cloud.ini
```

if you want to use a different path for the configuration file, you can specify it using the `--dns-hetzner-cloud-credentials` option when running Certbot.

## Usage
```bash
certbot certonly --agree-tos --authenticator dns-hetzner-cloud -d example.eu -d '*.example.eu'
```

## Troubleshooting

### T
If you encounter an error like:
```
Encountered exception during recovery: AttributeError: 'ExtractResult' object has no attribute 'top_domain_under_public_suffix'
An unexpected error occurred:
AttributeError: 'ExtractResult' object has no attribute 'top_domain_under_public_suffix'
```

This is likely due to an outdated version of the `tldextract` library. To resolve this issue, you can upgrade the library using pip:
```bash
/opt/certbot/bin/pip install -U --force-reinstall tldextract
```

[1]:https://github.com/ctrlaltcoop/certbot-dns-hetzner
[2]:https://certbot.eff.org/instructions