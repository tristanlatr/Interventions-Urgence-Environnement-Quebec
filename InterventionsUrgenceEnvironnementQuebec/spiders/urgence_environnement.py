from os import remove
from urllib.parse import urljoin
import scrapy
import abc
import time
from lxml import html
from ..utils import replace
from ..db import JsonDataBase

class Scraper_urgence_environnement(scrapy.Spider):

    name = "urgence_environnement"
    allowed_domains = ["www.environnement.gouv.qc.ca"]
    start_urls=['http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/archive.asp']

    def __init__(self, db=JsonDataBase(), parse_everything=False):
        super().__init__()
        self.db=db
        self.parse_everything = parse_everything

    def parse(self, response):
        """
        yields scrapy.Request

        @url http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/archive.asp
        @returns requests 1
        @scrape_not_none url evenement data_signalement num_dossier categorie lieu municipalite region matiere millieu etat
        """
        periods = self.get_periods_list(response)
        counter = 0
        
        for period in periods:

            yield scrapy.Request(period, callback=self.parse_interventions_list)
            
            counter += 1
            if not self.parse_everything and counter > 1:
                break

    def get_periods_list(self, response):
        """
        Read the "Archive du registre des interventions d'Urgence-Environnement" main archive page.
        Parse all links referring to every month since april 2008 until now. 

        Arguments:  
            - response: scrapy response object for the listing page
        
        Return a list of URLs
        
        @url http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/archive.asp
        @returns_valid_list_of_links
        """
        page = html.fromstring(response.text)

        return [ urljoin("http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/", ressource) 
            for ressource in page.xpath('/html/body/table[2]/tr/td[2]/table//a/@href') ]

    def parse_interventions_list(self, response):
        """
        Read a listing page of the "Archive du registre des interventions d'Urgence-Environnement". 
        Parse all links referring to every interventions of the given month. 

        Arguments:  
            - response: scrapy response object for the listing page
        
        yields scrapy.Request
        
        @url http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/index.asp?mois=5&annee=2020
        @returns requests 1
        """
        interventions = self.get_interventions_list(response)

        for intervention in interventions:
            
            # Load the intervention page only if it's new or it's not terminated yet
            if not self.db.search(intervention) or 'Termin' not in self.db.search(intervention)['etat']:
                
                yield scrapy.Request(intervention, callback=self.parse_intervention)

    def get_interventions_list(self, response):
        """
        Read a listing page of the "Archive du registre des interventions d'Urgence-Environnement". 
        Parse all links referring to every interventions of the given month. 

        Arguments:  
            - response: scrapy response object for the listing page
        
        Return a list of URLs
        
        @url http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/index.asp?mois=5&annee=2020
        @returns_valid_list_of_links
        """
        page = html.fromstring(response.text)

        return [ urljoin("http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/", ressource) 
            for ressource in page.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr//td[2]/a/@href') ]        

    def parse_intervention(self, response):
        """
        Read a intervention page of the "Archive du registre des interventions d'Urgence-Environnement". 
        Parse all informations regarding an emmergency intervention

        Arguments:  
            - response: scrapy response object for the intervention page 
        
        Retrurn a item object

        @url http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/urgence.asp?dossier=301465265
        @scrape_not_none url evenement data_signalement num_dossier lieu municipalite region matiere millieu etat
        @returns items 1 1  
        """

        sections_short_desc = {
            "Événement":                                            "evenement",
            "Date":                                                 "data_signalement",
            "Numéro de dossier":                                    "num_dossier",
            # "Catégorie":                                            "categorie",
            "Lieu de l'événement":                                  "lieu",
            "Municipalité ou territoire":                           "municipalite",
            "Région administrative":                                "region",
            "Matière":                                              "matiere",
            "Milieu(x) touché(s)":                                  "millieu",
            "Autres ministères":                                    "autre_organismes_public_implique",         # Facultative
            "État du dossier":                                      "etat",
            "Autres informations":                                  "autres_infos"  # Facultative
        }
        """
        Mapping of the fielde description (in the urgence_environnement application) and fields name (in the python object)
        """

        infos = {
            'url':          response.url, 
            'evenement':    None, 
            'data_signalement':         None, 
            'num_dossier':  None, 
            'categorie':    None, 
            'lieu':         None, 
            'municipalite': None, 
            'region':       None, 
            'matiere':      None, 
            'millieu':      None, 
            'autre_organismes_public_implique':         None, 
            'etat':         None, 
            'autres_infos': None
        }

        page = html.fromstring(response.text)

        rows = page.xpath('/html/body/table[2]/tr/td[2]/table//tr')
        if not rows:
            raise RuntimeError("Cannot parse rows from intervention page. The page HTML is :\n{}".format(response.text))

        for row in rows:
            for description in sections_short_desc.keys():

                field_desc = ''.join(row.xpath('td[1]/text()'))

                if description in field_desc:

                    key = sections_short_desc.get(description)
                    
                    # Special case #1
                    if key == 'evenement':
                        infos[key] = row.xpath('td[2]/strong/text()').pop()
                    
                    # Special case #2
                    elif key == 'num_dossier':
                        results = row.xpath('td[2]/text()')
                        infos['categorie'] = results.pop().replace(":","").strip()
                        infos[key] = results.pop()

                    else:
                        infos[key] = ''.join(row.xpath('td[2]/text()'))

        # Postprocess 
        for k,v in infos.items():
            if v:
                infos[k] = replace( v, {'\t':'', '\n':'', '\r':''} ).strip()

        return infos