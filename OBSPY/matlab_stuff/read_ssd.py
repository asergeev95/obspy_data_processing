from scipy.io import loadmat
import numpy as np
import pandas as pd
import os

path = r'C:\Users\loginovgn\Downloads\100'
cols = ['station', 'network', 'channel', 'Phase', 'Time', 'Level',
       'Quality', 'Sign', 'Distance', 'Azimuth']

path2save = r'C:\Users\loginovgn\Downloads\100_csv'
for file in os.listdir(path):
    file2save = file.split('.')[0] + '.csv'

    data = loadmat(
        os.path.join(path, file), 
        mat_dtype=True, 
        chars_as_strings=True, 
        squeeze_me=True
    )
#     print(1)
    data = data['Data']

    df = pd.DataFrame(
        np.array(data['ARRIVAL'], ndmin=1)[0].T,
        columns=[
            'station', 'network', 'channel', 'fullname', 'Phase',
            'Time', 'Level', 'Quality', 'Sign', 'DistAz'
        ]
    )
    df['Distance'] = df['DistAz'].apply(lambda x: x.split(';')[0])
    df['Azimuth'] = df['DistAz'].apply(lambda x: x.split(';')[1])

    df[cols].to_csv(
        os.path.join(path2save, file2save),
        sep=',',
        index=False,
    )