# Custom Ambilight integration for Home Assistant

![installation_badge](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.custom_ambilight) ![hassfest](https://github.com/aegjoyce/custom-ambilight/workflows/hassfest/badge.svg) ![hacs](https://github.com/aegjoyce/custom-ambilight/workflows/hacs/badge.svg)

## Why does this exist?
The core PhilipsJS integration is fantastic but has a few issues:
 - The JointSpace API on Philips TVs is fragile and temperamental - it doesn't like having lots of API calls in quick succession and can slow down or crash the TV after a while
 - The Ambilight implementation does not work consistently with all effect types due to various quirks in the JointSpace API

This custom integration fixes the above issues by:
 - Rate-limiting requests to the API and resetting the connection if needed
 - Providing workarounds for Ambilight mode-switching quirks

It also:
 - Enables the use of all Ambilight modes including modes hidden in the TV UI

## How do I install it?
Currently this integration requires:
 - A Philips Ambilight TV running version 6 of the JointSpace API
 - The IP address of your TV
 - A paired username and password for your TV, obtained using [this script](https://github.com/suborb/philips_android_tv/tree/master)

It is also highly recommended to set up the Alexa app and follow the instructions to keep the TV connected even when off.

Install via HACS, restart your Home Assistant, and then set up the Custom Ambilight integration in the UI.

## Future plans
 - Automatic registration from IP address without having to get a username and password
 - Support for other API versions
