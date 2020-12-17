import tempfile
import simplekml

def get_kml_file(items):
    with tempfile.NamedTemporaryFile(delete=False) as kml_file:
        kml = simplekml.Kml()
        fol = kml.newfolder(name='region 1') 
        # https://simplekml.readthedocs.io/en/latest/containers.html#simplekml.Folder
        # TODO classer par region / categorie and points
        pnt = fol.newpoint()
        # See arguments https://simplekml.readthedocs.io/en/latest/geometries.html#point
        # KML limits: https://support.google.com/earth/thread/20643937?hl=en
        # The JSON file if 3.6 MB
        # How to import the KML file https://support.google.com/earth/answer/7365595?hl=en&co=GENIE.Platform=Desktop
        return None
