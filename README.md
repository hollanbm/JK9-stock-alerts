# JK9-stock-alerts

Simple python script for checking stock of items on [Julius K9](https://usa.juliusk9.com/)

* [Poetry](https://python-poetry.org/) for dependency management
* Selenium Chrome Driver for headless web browsing to render page
* Push notifications via [Pushover.net](https://pushover.net/api)
* Dynaconf for secrets and settings
  * Don't forget to set the pushover token/keys in `.secrets.toml`
