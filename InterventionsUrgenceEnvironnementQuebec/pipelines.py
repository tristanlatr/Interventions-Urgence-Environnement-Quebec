# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from geopy.geocoders import Nominatim, GeoNames, Bing, Photon
import time
import os

class AddKeywordMatchesPipeline(object):
    
    
    matches=list(set([   

        # List extracted with keyword analysis from InterventionsUrgenceEnvironnementQuebec.json: 
        
        "déversement", "produits pétroliers", "coloration", "hydrocarbures", "résidus", "matières dangereuses", 
        "odeur", "huile", "eaux usées", "gaz", "fuite", "moteur", "diesel", "pneus", "eaux de procédé", "matières résiduelles",
        "ciment", "distillat", "milieu humide", "hydrique", "eau", "rivière", "sol", "air", "infrastructure", "souterraine", "surface",
        "ministère des transports", "sûreté du québec", "suivi", "travaux", "réservoir"

        # English and French keywords for general green job findings 

        "climate", "animal", "wildlife", "biomass", "pollution", "conservation", "biodiversity", 
        "nature", "ecotourism", "sustainable", "renewable", "energy", "education", "food",
        "agriculture", "organic", "farming", "forest", "green", "social",  "business", "entrepreneurship", 
        "leadership", "media", "journalism", "food security", "health", "ocean", "bike", "recycle", "waste",
        "intership"
        
        "climat", "animal", "faune", "biomasse", "pollution", "conservation", "biodiversité", 
        "nature", "écotourisme", "durable", "renouvelable", "énergie", "éducation", "alimentation",
        "agriculture", "biologique", "agriculture", "forêt", "vert", "social", "entreprise", "esprit d'entreprise", 
        "leadership", "médias", "journalisme", "sécurité alimentaire", "santé", "océan", "vélo", "recyclage", "déchets",
        "stage"

    ]))
    
    def process_item(self, item, spider):
        
        item['keywords_matched'] = [ m for m in self.matches if m in str(repr(item)).lower() ]
        
        return item

class AddGeocodePipeline(object):
    """
    Fill the 'latitude' and 'longitude' of all `Urgence` objects with no geoloc yet. 

    This code respects the Nominatim policy https://operations.osmfoundation.org/policies/nominatim/
    """

    def _geocode(self, lieu, municipalite, coder):
        time.sleep(1)
        resp = coder.geocode("{}, {}, Québec, Canada".format(lieu, municipalite),
            exactly_one=True
            )

        if resp:
            return (resp.latitude, resp.longitude)
        else:
            return None


    def geocode(self, lieu, municipalite, region):
        """
        Look for env variable 'BING_MAPS_KEYS' to init bing maps coder
        """

        coders = []
        
        bing_key = os.environ.get('BING_MAPS_KEYS', None)
        if bing_key:
            coders.append( Bing(api_key=bing_key) )
       
        coders.append( Photon(user_agent="Interventions-Urgence-Environnement-Quebec") )
        coders.append( Nominatim(user_agent="Interventions-Urgence-Environnement-Quebec", ) )

        result = None

        for i, c in enumerate(coders):
            
            result = self._geocode(lieu, municipalite, coder=c)
            if result:
                return(result)


    def process_item(self, item, spider):
        # Use geopy https://geopy.readthedocs.io/en/latest/#nominatim
        
        resp = self.geocode(item['lieu'], item['municipalite'], item['region'])
        if resp:
            item['latitude'] = resp[0]
            item['longitude'] = resp[1]
        else:
            item['latitude'] = 'Error'
            item['longitude'] = 'Error'
        return item
