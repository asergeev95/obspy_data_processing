from obspy import read
from obspy.core.stream import Stream
import pandas as pd
import os
import numpy as np

def process_data():
    msdSt = Stream()
    gcfSt = Stream()
    for filename in os.listdir():
        if filename.endswith(".msd"):
            msdSt += read(filename)
        if filename.endswith(".gcf"):
            gcfSt += read(filename)

    msdSt.merge()
    gcfSt.merge()

    msdDataFrame=pd.DataFrame(data = msdSt[0].data)
    gcfDataFrame = pd.DataFrame(data=gcfSt[0].data)
    return msdDataFrame, gcfDataFrame

process_data()