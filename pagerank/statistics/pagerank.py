import json
import numpy as np


def calculate_pagerank(links_map_file):
    with open(links_map_file, "r") as f:
        links_data: dict = json.load(f)

    links_map = {link_dict["parent"]: link_dict["children"] for link_dict in links_data}

    total_links = []
    for parent, children in links_map.items():
        total_links.append(parent)
        total_links += children

    for link in total_links:
        if link not in links_map.keys():
            connected_links = []
            for parent, children in links_map.items():
                if link in children:
                    connected_links.append(parent)
            links_map[link] = connected_links

    link_names = list(set(total_links))
    set_len = len(link_names)

    m = np.zeros(shape=(set_len, set_len))

    print(f"matrix len {set_len}x{set_len}")
    for i in range(set_len):
        for j in range(set_len):
            if link_names[j] in links_map[link_names[i]]:
                m[i][j] += 1.0/len(links_map[link_names[j]])
                print(f"[{i}][{j}]: {m[i][j]}")

    coef = np.full((set_len,), 1.0/set_len)
    print(coef)

    weights = np.matmul(coef, m)

    weights_map = {}
    for links_name, weight in zip(link_names, weights):
        weights_map[links_name] = weight

    with open("soundcloud_pagerank.json", "w") as f:
        json.dump(weights_map, f)

    sorted_weight_map = sorted(weights_map.items(), key=lambda x: x[1], reverse=True)
    print(sorted_weight_map)

    with open("soundcloud_links_sorted.txt", "w") as f:
        for items in sorted_weight_map:
            print(f"{items[0]}: {items[1]}", file=f)


if __name__ == "__main__":
    calculate_pagerank("../pagerank/soundcloud_links.json")
