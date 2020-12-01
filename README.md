[![Linux/Mac/Windows build status](
  https://circleci.com/gh/dwave-examples/structural-imbalance.svg?style=svg)](
  https://circleci.com/gh/dwave-examples/structural-imbalance)

# Structural Imbalance in Signed Social Networks

*Social networks* map relationships between people or organizations onto
graphs, with the people/organizations as nodes and relationships as edges; for
example, Facebook friends form a social network with friends represented as
nodes with connecting edges. *Signed social networks* map both friendly and
hostile relationships by setting the values of the edges between nodes with
either plus ("+") or minus ("-") signs. Such networks are said to be
*structurally balanced* when they can be clearly divided into two, with
friendly relations (represented by positive-valued edges) in each faction, and
hostile relations (negative-valued edges) between these factions.

The measure of *structural imbalance* or *frustration* for a signed social
network is the minimum number of edges that violate this rule.

![Three-person social network](_static/Social.png)

Social theory suggests that increased frustration predicts social instability.
In the context of militant organizations, this can result in increased
violence.

This demo calculates and shows structural imbalance for social networks of
militant organization based on data from the [Stanford Militants Mapping
Project](http://web.stanford.edu/group/mappingmilitants/cgi-bin/).

## Usage

To run the demo, execute one of the following two commands:

### A. Local CPU Execution

```bash
python structural_imbalance.py --cpu
```

### B. D-Wave System Execution

```bash
python structural_imbalance.py --qpu
```

## Code Specifics

The demo fetches data from the Stanford Militants Mapping Project, calculates
the networks, and saves a PNG graphic file of the imbalance network in the root
directory of your copy of the demo repository.

Additional command line arguments are available to control the behavior of the
demo, such as the region that is considered and whether to display a plot rather
than saving a PNG file.  Information about the command options is available via:

```bash
python structural_imbalance.py --help
```

## License

The translation and solving code is released under the Apache License 2.0. See
[LICENSE](LICENSE) file.

The dataset is used with permission from the Stanford Militants Mapping
Project.

## References

Mapping Militant Organizations, Stanford University, last modified February 28,
2016, http://web.stanford.edu/group/mappingmilitants/cgi-bin/.
