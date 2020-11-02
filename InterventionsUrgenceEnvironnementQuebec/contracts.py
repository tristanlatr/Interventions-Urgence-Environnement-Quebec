

import re
from itemadapter import is_item, ItemAdapter
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.selector import Selector

class ScrapeNotNone(Contract):

    """ Contract to check presence of fields in scraped items and check if they are None

        @scrape_not_none url title description
    """

    name = 'scrape_not_none'

    def post_process(self, output):
        for x in output:
            if is_item(x):
                missing = [arg for arg in self.args if arg not in ItemAdapter(x) or ItemAdapter(x)[arg]==None]
                if missing:
                    missing_str = ", ".join(missing)
                    raise ContractFail("Missing or None fields: %s. Item is %s" % (missing_str, x))

class ReturnsValidLink(Contract):
    
    """ Contract to check if the method returns a valid link

        @returns_valid_link
    """

    name = 'returns_valid_link'

    def post_process(self, output):
        if output:
            output=output[0]
        if not isinstance(output, str):
            raise ContractFail("Output is not a valid String. Output is {}".format(output))
        if len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)) < 1:
            raise ContractFail("Output is not a valid link. Output is {}".format(output))

class ReturnsValidListOfLinks(Contract):
    
    """ Contract to check if the method returns a valid link

        @returns_valid_list_of_links
    """

    name = 'returns_valid_list_of_links'

    def post_process(self, output):
        if not isinstance(output, list):
            raise ContractFail("Output is not a valid list. Output is {}".format(output))
        if not output:
            raise ContractFail("The list is empty !")
        for link in output:
            if not isinstance(link, str):
                raise ContractFail("Output is not a valid String. Output is {}".format(link))
            if len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link)) < 1:
                raise ContractFail("Output is not a valid link. Output is {}".format(link))