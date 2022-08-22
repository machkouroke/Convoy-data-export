import pandas as pd
from utilities import was_were


class CsvCorrector:
    """
    Correct a csv file and return a version of the file with corrected values
    """

    def __init__(self, base_path: str, extension: str):
        self.base_path: str = base_path
        self.extension: str = extension

    @property
    def file_name(self):
        return f'{self.base_path}.{self.extension}'

    def csv_read(self) -> tuple[pd.DataFrame, str]:
        """
        Read a csv file and return a dataframe and the base path
        If the file is Excel file it read the Vehicles sheet and convert it to csv
        :return:
        """
        if self.extension == "xlsx":
            my_df: pd.DataFrame = pd.read_excel(rf'{self.base_path}.xlsx', sheet_name='Vehicles', dtype=str)
            my_df.to_csv(rf'{self.base_path}.csv', header=True, index=False)
            number_of_rows: int = my_df.shape[0]
            print(f'{number_of_rows} line{was_were(number_of_rows)} added to {self.base_path}.csv')
        return pd.read_csv(rf'{self.base_path}.csv'), self.base_path

    @staticmethod
    def correct_row(column: pd.Series) -> pd.Series:
        """
        Delete all non-numeric characters from a column
        :param column: The column to correct
        :return: The colonne with corrected values or the original column if no correction was done
        """
        return column.str.replace(r"\D", "").astype(int) if column.dtype == "object" else column

    @staticmethod
    def number_of_invalid_element(column: pd.Series) -> int:
        """
        Return the number of invalid elements in a column
        :param column: The column to check
        :return: The number of invalid elements in the column
        """
        return column.str.contains(r"\D").sum()

    def save(self, df: pd.DataFrame) -> str:
        """
        Save the corrected dataframe in a csv file
        :param df: The dataframe with corrected values
        :return: The file in which the dataframe was saved
        """
        corrected_file_name: str = rf'{self.base_path}[CHECKED].csv'
        df.to_csv(corrected_file_name, header=True, index=False)
        return corrected_file_name

    def init(self) -> None:
        """
        This function initialize the csvCorrector class
        """
        my_df, base_path = self.csv_read()
        incorrect_cells = my_df.apply(self.number_of_invalid_element, axis=1).sum()
        checked_df: pd.DataFrame = my_df.apply(self.correct_row, axis=0)
        new_file_name: str = self.save(checked_df)
        print(f"{incorrect_cells} cells were corrected in {new_file_name}")
        return None
