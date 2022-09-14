import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join


def make_graphs():

    data = pd.read_excel('ready_data.xlsx', sheet_name='tz_data')

    for area in np.unique(data['area']):
        graph = make_graph_for_cluster(data[data['area'] == area])
        if area == "ar\\vr":
            path = join('graphs', 'ar_vr.png')
        else:
            path = join('graphs', f'{area}.png')
        plt.title(area, fontdict={'fontsize': 'x-large', 'fontweight': 'bold'})
        plt.savefig(path, dpi=100)


def make_graph_for_cluster(area):

    clusters = np.unique(area['cluster'])

    # Draw Plot for Each Cluster
    plt.figure(figsize=(15, 15), dpi=100, facecolor='w', edgecolor='k')

    for cluster in clusters:
        x = area[area['cluster'] == cluster]['x']
        y = area[area['cluster'] == cluster]['y']

        color = np.unique(area[area['cluster'] == cluster]['color'])
        annotations = [split_text(keyword)
                       for keyword in area[area['cluster'] == cluster]['keyword']]
        cluster_name = np.unique(area[area['cluster'] == cluster]['cluster_name'])[0]
        size = [count / 5 for count in area[area['cluster'] == cluster]['count']]

        plt.scatter(x=x, y=y, s=size, c=color, label=cluster_name, linewidths=0.8, edgecolors='black')
        plt.legend(title='Кластеры', fontsize='small', scatteryoffsets=[0.5],
                   markerscale=0.4, markerfirst=False)

        for i, label in enumerate(annotations):
            plt.annotate(label, ((x.to_list())[i], (y.to_list())[i]),
                         ha='center', va='center')

    plt.axis('off')

    return plt


def split_text(string):  # split long string in two short with line break
    if len(string) < 15:
        return string
    words = string.split()
    count = len(words)
    result_string = ''
    for word in range(count):
        if len(result_string) >= 10 or word == count-1:
            result_string += '\n' + ' '.join(words[word:])
            return result_string
        result_string += (words[word] + ' ')


if __name__ == '__main__':
    make_graphs()
