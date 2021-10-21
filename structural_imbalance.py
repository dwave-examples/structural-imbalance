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

import click
import matplotlib
# Trap errors with importing pyplot (for testing frameworks) and
# specify "agg" backend
try:
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib.use("agg")
    import matplotlib.pyplot as plt

import dimod
import dwave.inspector
import dwave_networkx as dnx

from neal import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler

from drawing import draw_social_network
from mmp_network import global_signed_social_network


@click.command()
@click.option('--qpu', 'sampler_type', flag_value='qpu',
              help='Use the QPU')
@click.option('--cpu', 'sampler_type', flag_value='cpu',
              help='Use simulated annealing')
@click.option('--hybrid', 'sampler_type', flag_value='hybrid',
              help="Use Leap's hybrid sampler")
@click.option('--region', default='global',
              type=click.Choice(['global', 'iraq', 'syria'],
                                case_sensitive=False))
@click.option('--show', is_flag=True,
              help="show the plot rather than saving it")
@click.option('--inspect', is_flag=True,
              help=("inspect the problem with the D-Wave Inspector, "
                    "does nothing when not using the QPU with --qpu"))
def main(sampler_type, region, show, inspect):

    if sampler_type is None:
        print("No solver selected, defaulting to hybrid")
        sampler_type = 'hybrid'

    # get the appropriate signed social network
    G = global_signed_social_network(region=region)

    # choose solver and any tuning parameters needed
    if sampler_type == 'cpu':
        params = dict(num_reads=100)
        sampler = SimulatedAnnealingSampler()

    elif sampler_type == 'hybrid':
        params = dict()
        sampler = LeapHybridSampler()

    elif sampler_type == 'qpu':
        params = dict(num_reads=100,
                      chain_strength=2.0,
                      )
        sampler = dimod.TrackingComposite(EmbeddingComposite(DWaveSampler()))

    else:
        raise RuntimeError("unknown solver type")

    # use the chosen sampler (passing in the parameters)
    edges, colors = dnx.structural_imbalance(G,
                                             sampler,
                                             label='Example - Structural Imbalance',
                                             **params)

    if inspect and sampler_type == 'qpu':
        dwave.inspector.show(sampler.output)

    print("Found", len(edges), 'violations out of', len(G.edges), 'edges')

    draw_social_network(G, colors)

    if show:
        plt.show()
    else:
        filename = 'structural imbalance {} {}.png'.format(sampler_type, region)
        plt.savefig(filename, facecolor='white')
        plt.clf()


if __name__ == '__main__':
    main()
