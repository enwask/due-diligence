# Due Diligence

Due Diligence is your AI-powered shopping helper. Developed for the Knight Hacks 2023 hackathon using Flask, several
Google Cloud services and the Microsoft Semantic Kernel with GPT-3.5 Turbo.

This web application allows you to search for a type of product and gives you a digestible comparison of resulting
products and their specifications. You can also save products to your own personal list for later viewing and share your
list with others, or browse through your comparison history if you forgot to save a comparison result.

As a bonus of custom scraping for product search results, we ignore sponsored products and ads by default, giving you
organic product results that you can trust.

## Tech specs

Due Diligence makes use of the following technologies:

* [Flask](https://github.com/pallets/flask) with Python 3.9 for routing and server-side logic
* HTML, Javascript and [LessCSS](https://lesscss.org/) (compiled to CSS on push
  by [this GitHub Actions workflow](.github/workflows/deploy.yaml))
* The [Schema UI framework](https://github.com/danmalarkey/schema) for some handy layout components and CSS boilerplate
* The [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) with GPT-3.5 Turbo for comparing
  products
* [Oxylabs' E-Commerce Scraper](https://docs.oxylabs.io/wmw8gbrbnajdf87/scraper-apis/e-commerce-scraper-api) for product search results
* [Google App Engine](https://cloud.google.com/appengine) for serverless hosting of the Flask app
* [Cloud Build](https://cloud.google.com/build) and [GitHub Actions](https://github.com/enwask/due-diligence/actions) for
  CI/CD
* *~~Google's [Programmable Search Engine](https://programmablesearchengine.google.com/about/) for product search results to
  feed to the AI model~~ (unused in the final iteration)*