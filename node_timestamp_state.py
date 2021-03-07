import pandas as pd
import os
from datetime import datetime

def behavior_states(df, t, x_source, x_target, slider_t=None):
    """ Return the states of nodes. Useful when you want to showcase lineage
    and implement a timeslider with which you want to determine whether nodes or edges
    of the graph are already active, passive or already completed.

    Keyword arguments:
    df -- A pandas DataFrame which contains the node links and their timestamp
    t -- The column contemplating the timestamp
    x_source -- The "from" node which links to the target node
    x_target -- The target node
    slider_t -- The value of a timeslider in the graph.
    """

    df[t] = pd.to_datetime(df[t])

    min_dates_source = df.groupby([x_source])[t].min()
    min_dates_target = df.groupby([x_target])[t].min()
    max_dates_source = df.groupby([x_source])[t].max()
    max_dates_target = df.groupby([x_target])[t].max()

    min_dates = min_dates_source.combine(min_dates_target, min)
    max_dates = max_dates_source.combine(max_dates_target, max)

    min_dates = min_dates.to_frame()
    min_dates.index.names = ['nodes']
    max_dates = max_dates.to_frame()
    max_dates.index.names = ['nodes']

    result = pd.merge(min_dates,max_dates,on='nodes',how='outer', suffixes=('_min','_max'))
    result[t + '_min'] = result[t + '_min'].fillna(value='2000-01-01 09:00:00')
    result[t + '_max'] = result[t + '_min'].fillna(value='2000-01-01 09:00:00')

    result[t + '_min'] = pd.to_datetime(result[t + '_min'])
    result[t + '_max'] = pd.to_datetime(result[t + '_max'])

    result.loc[result[t + '_max'] <= slider_t, 'state'] = 'completed'
    result.loc[result[t + '_min'] >= slider_t, 'state'] = 'passive'
    result.loc[(result[t + '_min'] <= slider_t) & (result[t + '_max'] >= slider_t), 'state'] = 'active'

    return result

def test_function():
    """ This function generates some testdata and a test slider-t value
        which will be used for testing the behavior_states functionality"""

    d = {
        'from': ['a1', 'a2', 'a3', 'a4'],
        'to': ['b2', 'b3', 'b4', 'b2'],
        'timestamp': ['2020-01-24 13:46:23', '2020-01-25 13:46:23', '2020-01-26 13:46:23', '2020-01-27 13:46:23']
    }

    df = pd.DataFrame(d)
    timestamp_slider = pd.to_datetime('2020-01-26 13:45:12')

    print(f'For testing the slider value is set to be: {timestamp_slider}')

    return behavior_states(df, 'timestamp', 'from', 'to', slider_t=timestamp_slider)

if __name__ == '__main__':
    print(f'Running test function...')
    try:
        print(test_function())
        print(f'Test run was succesful!')
    except:
        print(f'Test run was not succesful!')
