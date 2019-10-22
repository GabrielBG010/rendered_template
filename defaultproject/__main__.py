# import hashlib
import os
import pandas as pd

from defaultproject.io import atomic_write
from .hash_str import get_csci_salt, get_user_id, hash_str


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


if __name__ == "__main__":

    for user in ["gorlins", "GabrielBG010"]:
        print("Id for {}: {}".format(user, get_user_id(user)))

    data_source = "./data/hashed.xlsx"

    # TODO: read in, save as new parquet file, read back just id column, print

    # Reading of the excel file
    df = pd.read_excel(data_source)

    # obtainig the filename and the file extension
    filename, file_extension = os.path.splitext(data_source)

    # creating the name of the file
    new_filename = filename + ".parquet"

    # atomic write of the file
    with atomic_write(new_filename, "w") as f:
        df.to_parquet(f.name, engine='pyarrow')

    # reading of the file
    df2 = pd.read_parquet(new_filename,
                          engine='pyarrow', columns=["hashed_id"])
