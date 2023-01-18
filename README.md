# Subserv
Subserv is a simple redirect server which works for multiple domains. Simply point A records for @ and * to your server, and edit from config.json. This works great as a catch-all for Apache or similar web servers.

## Installing
Set the main.py file to auto-run on boot (the working directory must contain the config file)

## Known issues
- As of right now, you must restart the server for your config changes to take effect.
