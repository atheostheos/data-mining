from pyvis.network import Network
import json


def make_graph(links_map_file):
    with open(links_map_file, "r") as f:
        links_map: dict = json.load(f)

    net = Network(height='1000px', width='100%', bgcolor='#222222', font_color='white')
    net.barnes_hut()
    net.toggle_physics(False)
    for links_dict in links_map:
        parent = links_dict["parent"]
        children = links_dict["children"]
        net.add_node(parent, parent)
        for child in children:
            net.add_node(child, child)
            net.add_edge(parent, child)

    net.show("soundcloud_no_physics.html")


if __name__ == "__main__":
    make_graph("../../pagerank/soundcloud_links.json")
