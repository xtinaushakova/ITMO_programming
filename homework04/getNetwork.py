# -*- coding: utf-8 -*-
import requests
import time
import igraph
import datetime
from igraph import Graph, plot
from config import config
from api import get_friends

def get_network(users_ids, as_edgelist=True):
    edges = []
    matrix = [[0 for j in range(len(users_ids))]
              for i in range(len(users_ids))]

    for i, user_id in enumerate(users_ids):
        date1 = datetime.datetime.now()
        response = get_friends(user_id)
        if response.get('error'):
            continue
        friends_list = response['response']['items']
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends_list:
                if as_edgelist:
                    edges.append((i, j))
                else:
                    matrix[i][j] = matrix[j][i] = 1
        date2 = datetime.datetime.now()
        time.sleep(max(0, 0.33334 - (date2 - date1).total_seconds()))
    if as_edgelist:
        return edges
    else:
        return matrix

def get_network(user_id):
    response = get_friends(user_id)
    friends_list = response.get('response').get('items')
    vertices = [i for i in range(len(friends_list))]
    edges = get_network(friends_list)
    surnames = get_friends(user_id, 'last_name')['response']['items']
    vertices = [i['last_name'] for i in surnames]

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                       "label": vertices,
                                       "size": 2},
                         edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
            "vertex_label_dist": 5,
            "vertex_size": 2,
            "edge_color": "gray",
            "layout": g.layout_fruchterman_reingold(
                maxiter=100000,
                area=n ** 2,
                repulserad=n ** 2)
        }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, "friendNetwork.pdf", **visual_style)


if __name__ == '__main__':
    get_network(config.get('VK_ID'))