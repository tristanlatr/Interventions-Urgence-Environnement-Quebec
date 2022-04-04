- Clone the repository and run 

    pip install .

- Ensure that the package aiohttp is NOT installed: 

    pip uninstall aiohttp 

(solves TypeError: function() argument 'code' must be code, not str)

- Test it out

    scrapy check

- Usage

    python3 -m InterventionsUrgenceEnvironnementQuebec --help
