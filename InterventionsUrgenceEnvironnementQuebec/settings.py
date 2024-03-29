# Scrapy settings for InterventionsUrgenceEnvironnementQuebec project

BOT_NAME = 'InterventionsUrgenceEnvironnementQuebec'

SPIDER_MODULES = ['InterventionsUrgenceEnvironnementQuebec.spiders']

DOWNLOAD_DELAY = 2

COOKIES_ENABLED=False

DOWNLOADER_MIDDLEWARES={
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

FAKEUSERAGENT_FALLBACK='Mozilla'

SPIDER_CONTRACTS = {
    'InterventionsUrgenceEnvironnementQuebec.contracts.ScrapeNotNone': 10,
    'InterventionsUrgenceEnvironnementQuebec.contracts.ReturnsValidLink': 10,
    'InterventionsUrgenceEnvironnementQuebec.contracts.ReturnsValidListOfLinks': 10,
}

ITEM_PIPELINES={
    'InterventionsUrgenceEnvironnementQuebec.pipelines.AddKeywordMatchesPipeline': 100,
    'InterventionsUrgenceEnvironnementQuebec.pipelines.AddGeocodePipeline': 100
}
