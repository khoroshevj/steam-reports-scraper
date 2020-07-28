# About
Expose steam sales and wishlists CSV reports via an API endpoint. Scrapper requires your steam login/pass and code from the email to log in to https://partner.steampowered.com using Selenium WebDriver.

# Usage
Pass email and steam settings into container via `config.json` (see [example](/example.json)).

```
docker run -p 9000:9000 --mount type=bind,source=config.json,destination=/app/config.json registry.company.com:5000/sub/steam-reports-scraper:1.0.0
```

There is only one exposed endpoint `/report`. Report name (`sales` or `wishlists`) shall be passed as query parameter (e.g. `/report?name=sales`)

# Build & publish image
```
docker build -t registry.company.com:5000/sub/steam-reports-scraper:1.0.0 .
docker push registry.company.com:5000/sub/steam-reports-scraper:1.0.0
```