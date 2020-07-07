# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib.pyplot as plt
import networkx as nx


def draw_social_network(G, colors=None, pos=None):
    """Draw the given signed social network."""

    # get ordered nodelist and edgelist
    nodelist = list(G.nodes)
    edgelist = list(G.edges)

    if colors is not None:
        node_color = [colors[v] for v in nodelist]
        edge_color = [int(colors[u] == colors[v]) for u, v in edgelist]

        style = []
        for u, v in edgelist:
            if colors[u] != colors[v] and G[u][v]['sign'] > 0:
                style.append('dotted')
            elif colors[u] == colors[v] and G[u][v]['sign'] < 0:
                style.append('dotted')
            else:
                style.append('solid')

    else:
        node_color = None
        edge_color = None
        style = ['solid']*len(G.edges)

    # draw the the coloring
    nx.draw(G,
            node_size=100,
            pos=nx.circular_layout(G),
            cmap=plt.get_cmap('plasma'),
            edge_cmap=plt.get_cmap('RdYlGn'),
            edgelist=edgelist, nodelist=nodelist,
            width=2,
            node_color=node_color,
            edge_color=edge_color,
            edgecolors='black',
            style=style,
            )
