# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Urgence(scrapy.Item):

    # Mandatory Fields
    url = scrapy.Field() # response.url, 

    evenement = scrapy.Field()    
    date_signalement = scrapy.Field()         
    num_dossier = scrapy.Field()  
    categorie = scrapy.Field()    
    lieu = scrapy.Field()         
    municipalite = scrapy.Field() 
    region = scrapy.Field()       
    matiere = scrapy.Field()      
    millieu = scrapy.Field()      
    autre_organismes_public_implique = scrapy.Field()         
    etat = scrapy.Field()         
    autres_infos = scrapy.Field() 

    # Fields filled by post process
    latitude = scrapy.Field()    
    longitude = scrapy.Field() 
    geocoder_infos = scrapy.Field()

    # Fields filled by pipeline
    keywords_matched = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in Urgence.fields:
            self.setdefault(key, None)
