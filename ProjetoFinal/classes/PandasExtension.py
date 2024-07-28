import pandas as pd
import numpy as np
import io

class PandasExtension():
    def __init__(self, db:pd.DataFrame) -> None:
        self.db = db

    def info(self) -> pd.DataFrame:
        buffer = io.StringIO()
        self.db.info(buf=buffer, show_counts=True)
        lines = buffer.getvalue().split("\n")[3:-3]
        header_parts = lines[0].replace('Non-Null Count', 'Non-Null#Count').split(' ')[2:]
        header = [x.replace('#', ' ') for x in header_parts if len(x) > 0]
        header.append('Has Null')
        lines = lines[2:]
        
        data = []
        for x in lines:
            data.append([n for n in x.replace('non-null', '').split(' ')[2:] if len(n) > 0])

        max_val = 0
        for x in data:
            max_val = max(max_val, int(x[1]))

        for y, x in enumerate(data):
            data[y].append('True' if int(x[1]) != max_val else '')
        
        return pd.DataFrame(data, columns=header)

    def get_columns_except(self, names:list) -> list:
        return list(set(self.db.columns) - set(names))

    def print_column(self, name:str):
        lines = self.db[name].sort_values().unique()
        for x in lines:
            print(x)

    def list_column(self, name:str, splits:int) -> pd.DataFrame:
        lines = self.db[name].sort_values().unique()
        f = {}
        max_length = 0
        for x, i in enumerate(np.array_split(lines, splits)):
            i = list(i)
            f[x] = i
            max_length = max(len(i), max_length)
            while len(i) < max_length:
                i.append('')

        return pd.DataFrame(f).style.set_properties(**{'text-align': 'left', 'background-color': 'white'})

    def query_filter(self, query: str, cols: str) -> pd.DataFrame:
        return pd.DataFrame(self.db.query(query)[cols].sort_values().unique(), columns=[cols]).style.set_properties(**{'text-align': 'left'})