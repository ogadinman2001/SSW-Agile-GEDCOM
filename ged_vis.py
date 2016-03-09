import graphviz as gv

COLORS = ["yellow", "green", "blue", "violet"]

def graph_family(families, individuals, errors=None, anomalies=None):
    cid=0
    g1 = gv.Graph('Family Tree2', strict=True)
    g1.node_attr.update(color='lightblue2', style='filled')

    # Add node for every individual
    for indiv in individuals:
        if indiv.name:
            g1.node(' '.join(indiv.name))

    # Connect all spouses
    for family in families:
        wife = ' '.join(next(x.name for x in individuals if x.uid == family.wife))
        husb = ' '.join(next(x.name for x in individuals if x.uid == family.husband))
        children = family.children

        # For every spouse create a subgraph
        if wife and husb:
            if cid>=len(COLORS):
                cid=0

            g1.node(wife,color=COLORS[cid])
            g1.node(husb,color=COLORS[cid])
            cid += 1

        # Connect parents to children
        for child_uid in children:
            child = next(x for x in individuals if x.uid == child_uid)

            g1.edge(wife, ' '.join(child.name))
            g1.edge(husb, ' '.join(child.name))

    for error in errors:
        indiv = next((x for x in individuals if x.uid == error), None)
        if indiv:
            g1.node(' '.join(indiv.name), color ="red", shape='tripleoctagon')

    for anomaly in anomalies:
        indiv = next((x for x in individuals if x.uid == anomaly), None)
        if indiv:
            g1.node(' '.join(indiv.name), color ="orange", shape='tripleoctagon')

    g1.render(filename='tree')
