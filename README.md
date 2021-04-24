# ExchangeRate-API integration for Home Assistant

This integration returns currency rates from the [ExchangeRate-API](https://www.exchangerate-api.com/) api.

## Pre-requistes

1. Free API key from [exchangerate-api.com](https://www.exchangerate-api.com/)

## Installation

### HACS

1. Launch HACS
1. Navigate to the Integrations section
1. "+ Explore & Add Repositories" button in the bottom-right
1. Search for "exchangerate-api"
1. Select "Install this repository"
1. Restart Home Assistant

### Home Assistant

1. Go to the integrations page
1. Click on the "Add Integration" button at the bottom-right
1. Search for the "exchangerate-api" integration
1. Select the exchangerate-api integration

## Configuration

### Options

This integration can only be configuration through the UI (Configuration->Integrations), and the options below can be configured when the integration is added.

| key     | default | required | description                                          |
| ------- | ------- | -------- | ---------------------------------------------------- |
| api_key | none    | yes      | Your personal api key                                |
| base    | USD     | yes      | The base currency                                    |
| quote   | none    | yes      | The currency you want the rate vs. the base currency |

