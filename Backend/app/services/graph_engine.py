import networkx as nx
def build_network(user, beneficiary):
    g=nx.DiGraph(); g.add_node(f"user-{user.id}",label=user.name,type="USER",risk_level="LOW")
    g.add_node(f"beneficiary-{beneficiary.id}",label=beneficiary.name,type="BENEFICIARY",risk_level=beneficiary.risk_level)
    g.add_edge(f"user-{user.id}",f"beneficiary-{beneficiary.id}",relation="pays")
    if beneficiary.is_known_mule:
        for i in range(2):
            node=f"secondary-{beneficiary.id}-{i+1}"; g.add_node(node,label=f"Simulated Account {i+1}",type="MULE_ACCOUNT" if i==0 else "SECONDARY_ACCOUNT",risk_level="CRITICAL" if i==0 else "HIGH"); g.add_edge(f"beneficiary-{beneficiary.id}" if i==0 else f"secondary-{beneficiary.id}-1",node,relation="routes_to")
    return {"simulation":True,"nodes":[{"id":n,**d} for n,d in g.nodes(data=True)],"edges":[{"source":a,"target":b,**d} for a,b,d in g.edges(data=True)],"suspicious_connections":[e for e in g.edges() if "secondary" in e[1]]}
