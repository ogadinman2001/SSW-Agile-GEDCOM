""" Python module for parsing GEDCOM geneaology files - visualization

    This file provides the visualizations for the GEDCOM parsing project
"""

import graphviz as gv

COLORS = ["yellow", "green", "blue", "violet"]


def graph_family(families, individuals, errors=None, anomalies=None):
    """ Function used to generate visualization"""

    cid = 0
    fam_graph = gv.Graph('Family Tree2', strict=True, format='png')
    fam_graph.node_attr.update(color='lightblue2', style='filled')

    # Add node for every individual
    for indiv in individuals:
        if indiv.name:
            fam_graph.node(' '.join(indiv.name))

    # Connect all spouses
    for family in families:
        wife = ' '.join(next(x.name for x in individuals if x.uid == family.wife))
        husb = ' '.join(next(x.name for x in individuals if x.uid == family.husband))
        children = family.children

        # For every spouse create a subgraph
        if wife and husb:
            if cid >= len(COLORS):
                cid = 0

            fam_graph.node(wife, color=COLORS[cid])
            fam_graph.node(husb, color=COLORS[cid])
            cid += 1

        # Connect parents to children
        for child_uid in children:
            child = next(x for x in individuals if x.uid == child_uid)

            fam_graph.edge(wife, ' '.join(child.name))
            fam_graph.edge(husb, ' '.join(child.name))

    for error in errors:
        indiv = next((x for x in individuals if x.uid == error), None)
        if indiv:
            fam_graph.node(' '.join(indiv.name), color="red", shape='tripleoctagon')

    for anomaly in anomalies:
        indiv = next((x for x in individuals if x.uid == anomaly), None)
        if indiv:
            fam_graph.node(' '.join(indiv.name), color="orange", shape='tripleoctagon')

    fam_graph.render(filename='tree')
