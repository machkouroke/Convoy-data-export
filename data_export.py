import json
import sqlite3

import pandas as pd
from dicttoxml import dicttoxml
from lxml import etree

from utilities import was_were, scores


def data_add(conn, base_path: str) -> int:
    """
    Create a database for vehicles, compute scores for each vehicle and add them to the database
    :param conn: Connection object to the database
    :param base_path: base path of the file where the data is stored
    :return: The number of rows inserted into the database
    """
    conn.cursor().execute('Create table if not exists convoy '
                          '(vehicle_id INT,'
                          'engine_capacity INT ,'
                          'fuel_consumption INT,'
                          'maximum_load INT, '
                          'score INT)')
    convoy: pd.DataFrame = pd.read_csv(rf'{base_path}[CHECKED].csv')
    convoy["score"] = convoy.apply(scores, axis=1)
    convoy.to_sql('convoy', conn, if_exists='replace', index=False,
                  dtype={
                      'vehicle_id': 'INTEGER PRIMARY KEY',
                      'engine_capacity': 'INTEGER NOT NULL',
                      'fuel_consumption': 'INTEGER NOT NULL',
                      'maximum_load': 'INTEGER NOT NULL',
                      'score': 'INTEGER NOT NULL'
                  })

    return convoy.shape[0]


def convoy_select(conn, file_type: str = ""):
    """
    JSON file must contain vehicles with score > 3 and XML file must contain vehicles with score < 1
    So this function returns the data from the database that matches the file type
    :param conn: Connection object to the database
    :param file_type: The type of the file
    :return: The data matching the file type
    """
    cur = conn.cursor()
    without_score = "vehicle_id, engine_capacity, fuel_consumption, maximum_load"
    if not file_type:
        cur.execute('Select * from convoy')
    elif file_type == "JSON":
        cur.execute(f'Select {without_score} from convoy where score > 3')
    elif file_type == "XML":
        cur.execute(f'Select {without_score} from convoy where score <= 3')
    return cur.fetchall()


def db_to_dict(db_base_path: str, file_type: str = "") -> list:
    """
    Returns a list of dictionaries with the data from the database
    :param db_base_path: The base path of the database
    :param file_type: The type of the file to export
    :return: The list of dictionaries with the data from the database
    """
    conn = sqlite3.connect(rf'{db_base_path}.s3db')
    conn.row_factory = sqlite3.Row
    data = convoy_select(conn, file_type)
    return [dict(data) for data in data]


def export_sql(base_path: str) -> None:
    """
    Export the data from a given file of convoy to a database
    :param base_path: Base path of the file of convoy
    """
    db_name: str = rf'{base_path}.s3db'
    conn = sqlite3.connect(db_name)
    row_count: int = data_add(conn, base_path)
    conn.commit()
    print(f"{row_count} record{was_were(row_count)} inserted into {db_name}")
    conn.close()
    return None


def export_json(base_path: str) -> None:
    """
    Export the data from a given file of convoy to a JSON file
    :param base_path: The base path of the file of convoy
    """
    with open(f"{base_path}.json", "w") as convoy:
        all_convoy: dict = {"convoy": db_to_dict(base_path, "JSON")}
        json.dump(all_convoy, convoy)
        number_of_rows: int = len(all_convoy["convoy"])
        print(f"{number_of_rows} vehicle{was_were(number_of_rows)} saved into {base_path}.json")
    return None


def export_xml(base_path: str) -> None:
    """
    Export the data from a given file of convoy to a XML file
    :param base_path: The base path of the file of convoy
    """
    root = etree.Element("convoy")
    data = db_to_dict(base_path, "XML")
    for vehicle in data:
        root.append(etree.fromstring((dicttoxml(vehicle, custom_root="vehicle", attr_type=False))))
    etree.ElementTree(root).write(f"{base_path}.xml", pretty_print=True, method='html')
    number_of_rows: int = len(data)
    print(f"{number_of_rows} vehicle{was_were(number_of_rows)} saved into {base_path}.xml")
    return None
