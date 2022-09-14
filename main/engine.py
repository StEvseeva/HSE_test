import pandas as pd
import numpy as np
from numpy.random import randint
from functools import reduce


def main():
    data = pd.read_excel('test.xlsx', sheet_name='tz_data', na_values=['N\A', '-'])

    data.replace(to_replace='0x.*', value=None, regex=True, inplace=True)
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data.drop(columns='good (1)', inplace=True)
    print(data.dtypes)
    area_frames = prepare_areas(data.dropna())  # prepare areas and add colors for clusters

    result_data = reduce(add_frame, area_frames)  # concatenate areas in result frame
    result_data.sort_values(
            by=['area', 'cluster', 'count'],
            ascending=[True, True, False],
            inplace=True
        )

    write_to_excel(result_data)


def prepare_areas(data):

    prepared_areas = []
    areas = np.unique(data['area'])

    for area in range(len(areas)):
        prepared_areas.append(data[data['area'] == areas[area]].drop_duplicates(subset='keyword'))
        colors = generate_colors(prepared_areas[area]['cluster'])

        prepared_areas[area]['color'] = prepared_areas[area].apply(
            lambda x: get_color(x['cluster'], colors),
            axis=1
        )

    return prepared_areas


def generate_colors(clusters):

    colors = {}
    TABLEAU = ['#6dccda', '#cdcc5d', '#a2a2a2', '#ed97ca', '#a8786e', '#ad8bc9', '#ed665d']
    for cluster in np.unique(clusters):
        colors[cluster] = TABLEAU.pop(randint(0, len(TABLEAU)))

    return colors


def get_color(cluster, colors):
    return colors[cluster]


def add_frame(frame1, frame2):
    return pd.concat([frame1, frame2], axis=0, ignore_index=True)


def write_to_excel(frame):

    with pd.ExcelWriter('ready_data.xlsx', engine='xlsxwriter') as wb:
        frame.to_excel(wb, freeze_panes=(1, 0), sheet_name='tz_data', index=False)
        sheet = wb.sheets['tz_data']
        sheet.autofilter(0, 0, 0, 7)
        sheet.set_column('A:H', 10)
        sheet.set_column('C:D', 20)


if __name__ == '__main__':
    main()
