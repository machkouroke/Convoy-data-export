import os
from data_export import export_sql, export_json, export_xml
from csvCorrector import CsvCorrector

if __name__ == "__main__":
    print('Input file name')
    file_name: str = input()
    base_path, extension = os.path.splitext(file_name)
    if extension != ".s3db":
        if not file_name.endswith("[CHECKED].csv"):
            corrector: CsvCorrector = CsvCorrector(base_path, extension[1:])
            corrector.init()
        base_path = base_path.replace("[CHECKED]", "")
        export_sql(base_path)
    for pipeline in [export_json, export_xml]:
        pipeline(base_path)
