# Tim & Bastien - sumup

## create the .env file

```bash
cp api/env_example api/.env
```

## Get google credentials

Go to [console.cloud.google.com](console.cloud.google.com), open the api settings.

On the top left menu, open `APIs & Services->Credentials`. Download the `OAuth 2.0 Client IDs` named `Desktop client 1` and move the file in `api/credentials.json`.

## Get the sumup access token

Go to [sumup](https://me.sumup.com/dashboard) and open `Developeur` section (click on the top right name to see the section).

In `OAuth` section, download the `Export` file.

In the json downloaded file, copy the client_id and client_secret in the `api/.env` file