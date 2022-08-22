import json
import sqlite3
import pandas as pd

from lxml import etree
from dicttoxml import dicttoxml

from utilities import was_were, pit_stops, scores


def data_add(conn, base_path: str):
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


def db_to_dict(db_base_path: str, file_type: str = "") -> list:
    conn = sqlite3.connect(rf'{db_base_path}.s3db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    without_score = "vehicle_id, engine_capacity, fuel_consumption, maximum_load"
    if not file_type:
        cur.execute('Select * from convoy')
    elif file_type == "JSON":
        cur.execute(f'Select {without_score} from convoy where score > 3')
    elif file_type == "XML":
        cur.execute(f'Select {without_score} from convoy where score <= 3')
    return [dict(data) for data in cur.fetchall()]


def export_sql(base_path: str):
    db_name: str = rf'{base_path}.s3db'
    conn = sqlite3.connect(db_name)
    row_count: int = data_add(conn, base_path)
    conn.commit()
    print(f"{row_count} record{was_were(row_count)} inserted into {db_name}")
    conn.close()


def export_json(base_path: str):
    with open(f"{base_path}.json", "w") as convoy:
        all_convoy: dict = {"convoy": db_to_dict(base_path, "JSON")}
        json.dump(all_convoy, convoy)
        number_of_rows: int = len(all_convoy["convoy"])
        print(f"{number_of_rows} vehicle{was_were(number_of_rows)} saved into {base_path}.json")


def export_xml(base_path: str):
    root = etree.Element("convoy")
    data = db_to_dict(base_path, "XML")
    for vehicle in data:
        root.append(etree.fromstring((dicttoxml(vehicle, custom_root="vehicle", attr_type=False))))
    etree.ElementTree(root).write(f"{base_path}.xml", pretty_print=True, method='html')
    number_of_rows: int = len(data)
    print(f"{number_of_rows} vehicle{was_were(number_of_rows)} saved into {base_path}.xml")
