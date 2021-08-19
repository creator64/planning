import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData
import sqlalchemy

PATH = "datafiles/data.db"
T = "tbl"

def get_engine(path):
    engine = create_engine(f'sqlite:///{path}')
    return engine

def get_cols(path, tbn):
    engine = get_engine(path)
    df = pd.read_sql_query(f"SELECT * FROM {tbn} LIMIT 0", engine) # get pd dataframe without data (cuz we only need cols)
    return df.columns

def get_cls_from_table(path, tbn):
    engine = get_engine(path)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata.tables[tbn]

def add_row(path, tbn, **values):
    engine = get_engine(path)
    t = get_cls_from_table(path, tbn)
    st = t.insert().values(**values)
    engine.connect().execute(st)
    return 1

def add_col(path, tbn, new_col, TYPE="TEXT", default="NULL"):
    engine = get_engine(path)
    engine.execute(f"ALTER TABLE {tbn} ADD {new_col} {TYPE} DEFAULT {default}")
    return 1

def del_col(path, tbn, col_name):
    engine = get_engine(path)
    cols = get_cols(path, tbn) # get old columns
    new_cols = tuple(cols.delete(cols.get_loc(col_name))) # create new column list without the col we want to delete with pandas
    formatstr = ",".join(new_cols)

    engine.execute(f"CREATE TABLE backup AS SELECT {formatstr} FROM {tbn}")
    engine.execute(f"DROP TABLE {tbn}")
    engine.execute(f"ALTER TABLE backup RENAME TO {tbn}")
    return 1


def rename_col(path, tbn, col, new_col):
    engine = get_engine(path)
    engine.execute(f"ALTER TABLE {tbn} RENAME COLUMN '{col}' TO '{new_col}'")
    return 1

def remove_row(path, tbn, delete_table=False, **conditions):
    if not conditions and not delete_table: # preventing to delete the whole table
        print("function stopped becuase there were no conditions given and delete_table was set to False")
        return None
    engine = get_engine(path)
    t = get_cls_from_table(path, tbn)
    l = [t.c[condition] == conditions[condition] for condition in conditions]
    st = t.delete().where(*l)
    engine.execute(st)
    return 1


def update_table(path, tbn, col_value_dict, **conditions):
    engine = get_engine(path)
    t = get_cls_from_table(path, tbn)
    l = [t.c[condition] == conditions[condition] for condition in conditions]
    st = t.update().values(**col_value_dict).where(*l)
    engine.execute(st)
    return 1


#add_row(PATH, "tbl", [8924334289233, "dls-39238234", 232, "ui*HBK())()", "vluttie vlut", 3403203420, 44, 33])
#add_col(PATH, "tbl", "G", default="apen")
#del_col(PATH, "tbl", "B")
#rename_col(PATH, "tbl", "E", "J")

#remove_row(PATH, "tbl", D="buih£")
#conn, c= get_conn(PATH)
#c.execute("CREATE TABLE lol")
#print(c.fetchall())

#update_table(PATH, "tbl",
             #{"G": "bu",
              #"C": "vet"},
             #rowid=6, A="aap")
