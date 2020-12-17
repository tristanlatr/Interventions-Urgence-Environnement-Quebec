# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from geopy.geocoders import Nominatim, Bing
from ordered_set import OrderedSet
import time
import os
import logging
import geopy

loger = logging.getLogger(__name__)

class AddKeywordMatchesPipeline(object):
    
    matches=list(OrderedSet([   

        # List extracted with keyword analysis from InterventionsUrgenceEnvironnementQuebec.json: 
        
        "déversement", "produits pétroliers", "coloration", "hydrocarbures", "résidus", "matières dangereuses", 
        "odeur", "huile", "eaux usées", "gaz", "fuite", "moteur", "diesel", "pneus", "eaux de procédé", "matières résiduelles",
        "ciment", "distillat", "milieu humide", "hydrique", "eau", "rivière", "sol", "air", "infrastructure", "souterraine", "surface",
        "ministère des transports", "sûreté du québec", "suivi", "travaux", "réservoir",

        # English and French keywords for general green job findings 

        "climate", "animal", "wildlife", "biomass", "pollution", "conservation", "biodiversity", 
        "nature", "ecotourism", "sustainable", "renewable", "energy", "education", "food",
        "agriculture", "organic", "farming", "forest", "green", "social",  "business", "entrepreneurship", 
        "leadership", "media", "journalism", "food security", "health", "ocean", "bike", "recycle", "waste",
        "intership",
        
        "climat", "animal", "faune", "biomasse", "pollution", "conservation", "biodiversité", 
        "nature", "écotourisme", "durable", "renouvelable", "énergie", "éducation", "alimentation",
        "agriculture", "biologique", "agriculture", "forêt", "vert", "social", "entreprise", "esprit d'entreprise", 
        "leadership", "médias", "journalisme", "sécurité alimentaire", "santé", "océan", "vélo", "recyclage", "déchets",
        "stage",

    ]))
    
    def process_item(self, item, spider):
        
        item['keywords_matched'] = [ m for m in self.matches if m in str(repr(item)).lower() ]
        
        return item

class AddGeocodePipeline(object):
    """
    Fill the 'latitude' , 'longitude' and other gocoder infos objects. 

    Look for env variable 'BING_MAPS_KEYS' to init bing maps coder. 
    Add Nominatim coder as a backup. 
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.coders = []
        
        bing_key = os.environ.get('BING_MAPS_KEYS', None)
        if bing_key:
            self.coders.append( Bing(api_key=bing_key, timeout=10) )
        self.coders.append( Nominatim(user_agent="InterventionsUrgenceEnvironnementQuebec", 
            timeout=10) )

    def _geocode(self, lieu, municipalite, region, coder, retry=1):
        time.sleep(1)
        address_str = "{}, {} {}, Québec, Canada".format(lieu, municipalite, region)
        loger.info("Geocoding {} with coder {}".format(address_str, coder.__class__.__name__))

        try:

            resp = coder.geocode(address_str,
                exactly_one=True)
            if resp:
                return (resp.latitude, resp.longitude, resp.raw)
            else:
                loger.warning("Cannot find exact match for address {}".format(address_str))
                time.sleep(1)
                resp = coder.geocode(address_str,
                exactly_one=False)
                if resp:
                    return ('No exact match', 'No exact match', resp.raw)
                else:
                    loger.error("Geocoder {} cannot find any places for address {}".format(
                        coder.__class__.__name__, address_str))
                    return None
        
        except geopy.exc.GeocoderQuotaExceeded:
            return None
        except geopy.exc.GeopyError:
            if retry > 0:
                time.sleep(2)
                return self._geocode(lieu, municipalite, region, coder, retry=retry-1)
            else:
                return None

        

    def geocode(self, lieu, municipalite, region):
        """Resolve latitude, longitude and geocoder_infos or put 'Error'
        """
        result = None
        for _, coder in enumerate(self.coders):
            
            result = self._geocode(lieu, municipalite, region, coder=coder)
            if result:
                return result

    def process_item(self, item, spider):
        # Use geopy https://geopy.readthedocs.io/en/latest/
        
        resp = self.geocode(item['lieu'], item['municipalite'], item['region'])
        if resp:
            item['latitude'] = resp[0]
            item['longitude'] = resp[1]
            item['geocoder_infos'] = resp[2]
        else:
            item['latitude'] = 'Error'
            item['longitude'] = 'Error'
        return item
