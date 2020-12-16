import argparse
import shutil
import os
from .db import DEFAULT_DB_FILE, JsonDataBase
from .scrape import scrape
from .utils import get_xlsx_file

def get_parser():
    parser = argparse.ArgumentParser(
        description="""
        Interventions d'Urgence Environnement Quebec. 
        This software generates an Excel file (also JSON) containning all inforamtion from the Registre des interventions d'Urgence-Environnement Québec.
        The files will be placed in the same directory as the JSON databse. """,
        prog="python3 -m InterventionsUrgenceEnvironnementQuebec",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--db",
        metavar="<Path>",
        help='JSON Database file',
        default=DEFAULT_DB_FILE,
    )

    parser.add_argument(
        "--parse_everything",
        action="store_true",
        help="This will trigger complete parsing of every new (not in database) or not finished inteventions, from 2008. Default behaviour is only for testing. ",
    )

    return parser

def parse_args():
    return get_parser().parse_args()

def main():
    args = parse_args()

    db = JsonDataBase(filepath=args.db)

    data = scrape('urgence_environnement', scraper_init_kwargs={ 'db':db, 'parse_everything':args.parse_everything })

    new_data = db.update_and_write_items(data)

    if new_data:
        excel = get_xlsx_file(db.data)

        shutil.copyfile(excel.name, args.db + '.xlsx')
        os.remove(excel.name)

if __name__ == "__main__":
    main()
