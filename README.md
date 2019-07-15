# hv-datadog-plugins
Plugins for services in DataDog that are not natively supported.

# Sendgrid
## Description
Sendgrid publishes a wealth of metrics on their website from number of messages processed (hello licensing), blocks, spam reports, etc.  

Though they exist in a walled garden, sendgrid provides an API endpoint to exfiltrate the data. 

## Installation
 1. Drop the `hv_sendgrid.py` into `/etc/datadog-agent/checks.d/hv_sendgrid.py`
 1. Make the following directory: `/etc/datadog-agent/conf.d/hv_sendgrid.d/`
 1. Copy the `hv_sendgrid.yaml` to `/etc/datadog-agent/conf.d/hv_sendgrid.d/hv_sendgrid.yaml`
 1. Update `/etc/datadog-agent/conf.d/hv_sendgrid.d/hv_sendgrid.yaml` with the configuration values described below

## Configuration
This plugin expects an **instance configuration per [sub]account** in Sendgrid.  While they do have a "global" stats endpoint, it was unreliable and summarized the data too much.

To generate the API key for each [sub]user, login/switch to that user -> `Settings` -> `API Keys` -> `Create API Key`.  Select `Restricted Access` and grant the API key full `Stats` access.

| Configuration | Description |
|---------------|-------------|
| api_key | Generated, per [sub]user, at https://app.sendgrid.com/settings/api_keys |
| min_collection_interval | Time between polling the Sendgrid API.  Sendgrid appears to update their stats every 5min, so not worth going below 300 seconds. |
| account | This is acts as a tag for grouping/filtering metrics.  This should be set to an identifier for the billing unit |
| user | the [sub]username for which the API key was generated |
| tags | other logical tags for the metric |

### Example
```
init_config:

instances:
  - api_key: dfdfdfdf
    min_collection_interval: 300
    account: hirevue
    user: devmcdevface
    tags:
    - environment:dev
  - api_key: ababababa
    min_collection_interval: 300
    account: hirevue
    user: devpants
    tags:
    - environment:dev
  - api_key: cdcdcdcdcd
    min_collection_interval: 300
    account: hirevue
    user: fancyprodemail
    tags:
    - environment:prod
```

# Vault
## Description
While there exists a vault plugin it doesn't currently support the the requests counter api `sys/internal/counters/requests`.  The paid for version of Hashicorp Vault is licensed on a per-request basis, so tracking your requests can be beneficial.

It is worth noting that querying the health/status/requests with the DataDog increments your request count, which gets charged against your monthly total requests. Nothing is free.  So tune your collection internal accordingly.

## Installation
 1. Drop the `hv_vault.py` into `/etc/datadog-agent/checks.d/hv_vault.py`
 1. Make the following directory: `/etc/datadog-agent/conf.d/hv_vault.d/`
 1. Copy the `hv_vault.yaml` to `/etc/datadog-agent/conf.d/hv_vault.d/hv_vault.yaml`
 1. Update `/etc/datadog-agent/conf.d/hv_vault.d/hv_vault.yaml` with the configuration values described below

## Configuration

You'll need to configure a policy with in vault granting access to the endpoint
```
path "sys/internal/counters/requests" {
  capabilities = ["read", "list"]
}
```
From this policy generate a token that will be used to access the endpoint.


| Configuration | Description |
|---------------|-------------|
| token | The vault token |
| min_collection_interval | Since requests to the requests api count against your requests license set the collection interval to something sane. |

### Example
```
init_config:

instances:
  - token: VaultTokenHere
    min_collection_interval: 300
```
