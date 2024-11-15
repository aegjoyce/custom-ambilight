# Custom Ambilight
### An integration for Home Assistant

![stars](https://img.shields.io/github/stars/aegjoyce/custom-ambilight?style=flat&logo=github&logoColor=lightgrey&color=yellow) ![installation_badge](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.custom_ambilight.total) ![hassfest](https://github.com/aegjoyce/custom-ambilight/workflows/hassfest/badge.svg) ![hacs](https://github.com/aegjoyce/custom-ambilight/workflows/hacs/badge.svg)


### Why does this exist?
The core PhilipsJS integration is fantastic but has a few issues:
 - The JointSpace API on Philips TVs is fragile and temperamental - it doesn't like having lots of API calls in quick succession and can slow down or crash the TV after a while
 - The Ambilight implementation does not work consistently with all effect types due to various quirks in the JointSpace API

This custom integration fixes the above issues by:
 - Rate-limiting requests to the API and resetting the connection if needed
 - Providing workarounds for Ambilight mode-switching quirks

It also:
 - Enables the use of all Ambilight modes including modes hidden in the TV UI

### How do I install it?
Currently this integration requires:
 - A Philips Ambilight TV running version 6 of the JointSpace API
 - The IP address of your TV

It is also highly recommended to set up the Alexa app and follow the instructions to keep the TV connected even when off.

Install via HACS, restart your Home Assistant, and then set up the Custom Ambilight integration in the UI.
