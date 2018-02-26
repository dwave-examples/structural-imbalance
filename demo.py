from __future__ import division
import os

import dwave_qbsolv as qbsolv

import dwave_networkx as dnx

try:
    import dwave_micro_client_dimod as system
    _system = True
except ImportError:
    _system = False

import dwave_structural_imbalance_demo as sbdemo


def maps():
    Global = sbdemo.global_signed_social_network()

    # The Syria subregion
    syria_groups = set()
    for v, data in Global.nodes(data=True):
        if 'map' not in data:
            continue
        if data['map'] in {'Syria', 'Aleppo'}:
            syria_groups.add(v)
    Syria = Global.subgraph(syria_groups)

    # The Iraq subregion
    iraq_groups = set()
    for v, data in Global.nodes(data=True):
        if 'map' not in data:
            continue
        if data['map'] == 'Iraq':
            iraq_groups.add(v)
    Iraq = Global.subgraph(iraq_groups)

    return Global, Syria, Iraq


def diagramDateRange(directory_name, start, end, graph, sampler, subsolver, subarea=None, subarea_name=None):
    # Create directories
    directory_path = os.path.join('Results', directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Write .csv header line
    csv = open(os.path.join(directory_path, 'Structural Imbalance.csv'), 'w')
    csv.write('year,total groups,total edges,imbalanced edges,structural imbalance')
    if subarea is not None and subarea_name is not None:
        csv.write(',%s groups,%s edges,%s imbalanced edges,%s structural imbalance' % tuple([subarea_name] * 4))
    csv.write('\n')

    for year in range(start, end):
        # Compute structural imbalance up to and including year
        filtered_edges = ((u, v) for u, v, a in graph.edges(data=True) if a['event_date'].year <= year)
        subrange = graph.edge_subgraph(filtered_edges)
        imbalance, bicoloring = dnx.structural_imbalance(subrange, sampler, solver=subsolver)

        # Write stats to .csv
        num_nodes = len(subrange.nodes)
        num_edges = len(subrange.edges)
        num_imbalanced = len(imbalance)
        ratio = num_imbalanced / num_edges
        csv.write('%s,%s,%s,%s,%s' % (year, num_nodes, num_edges, num_imbalanced, ratio))
        if subarea is not None and subarea_name is not None:
            num_nodes = len(set.intersection(set(subrange.nodes), set(subarea.nodes)))
            num_edges = len(set.intersection(set(subrange.edges), set(subarea.edges)))
            num_imbalanced = len(set.intersection(set(imbalance), set(subarea.edges)))
            if num_edges != 0:
                ratio = num_imbalanced / num_edges
            else:
                ratio = '-'
            csv.write(',%s,%s,%s,%s' % (num_nodes, num_edges, num_imbalanced, ratio))
        csv.write('\n')

        # Draw graph
        file_name = 'Structural Imbalance %s.png' % year
        file_path = os.path.join(directory_path, file_name)
        sbdemo.draw(file_path, subrange, imbalance, bicoloring)
        print('output %s' % file_path)

    csv.close()


if __name__ == '__main__':
    # get a sampler
    sampler = qbsolv.QBSolv()

    if _system:
        print("Running on the QPU")
        subsolver = system.EmbeddingComposite(system.DWaveSampler())
    else:
        print("Running classically")
        subsolver = None

    # get the graphs
    Global, Syria, Iraq = maps()

    # calculate the imbalance of Global
    imbalance, bicoloring = dnx.structural_imbalance(Global, sampler, solver=subsolver)

    # draw the Global graph
    sbdemo.draw('syria_imbalance.png', Global, imbalance, bicoloring)

    # Images of the structural imbalance in the local Syrian SSN
    # for years 2010-2016 showing frustrated and unfrustrated edges.
    diagramDateRange('Syrian Theatre', 2010, 2016 + 1, Syria, sampler, subsolver)

    # Images of the structural imbalance in the world SSN for
    # years 2007-2016 showing frustrated and unfrustrated edges.
    diagramDateRange('World Network', 2007, 2016 + 1, Global, sampler, subsolver, Syria, 'Syria')
