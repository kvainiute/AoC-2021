import heapq


def find_path(graph):
    queue = []
    current_node = (0, 0)
    heapq.heappush(queue, (0, current_node))
    target_node = (max(x for x, y in graph.keys()), max(y for x, y in graph.keys()))
    risk = dict()
    risk[current_node] = 0
    while queue:
        current = heapq.heappop(queue)[1]
        if current == target_node:
            break
        for neighbor in get_neighbors(current, graph):
            new_risk = risk[current] + graph[neighbor]
            if neighbor not in risk or new_risk < risk[neighbor]:
                risk[neighbor] = new_risk
                priority = new_risk + manhattan_distance(neighbor, target_node)
                heapq.heappush(queue, (priority, neighbor))
    return risk[target_node]


def manhattan_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbors(node, graph):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    results = []
    for direction in directions:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if neighbor in graph:
            results.append(neighbor)
    return results


def new_cost(old_cost):
    if old_cost + 1 > 9:
        return 1
    else:
        return old_cost + 1


def parse_output(filename):
    file = open(filename, 'r')
    return {(x, y): int(cost) for y, line in enumerate(file.readlines()) for x, cost in enumerate(line.strip())}


def for_part_2(graph):
    to_add = max(x for x, y in graph.keys())

    prev_y = 0
    for y_rep in range(1, 5):
        new_graph = {(key[0], key[1] + to_add + 1): new_cost(cost) for key, cost in graph.items() if key[1] >= prev_y}
        graph.update(new_graph)
        prev_y += to_add

    prev_x = 0
    for x_rep in range(1, 5):
        new_graph = {(key[0] + to_add + 1, key[1]): new_cost(cost) for key, cost in graph.items() if key[0] >= prev_x}
        graph.update(new_graph)
        prev_x += to_add
    return graph


def main():
    graph = parse_output('input.txt')
    print("Part 1: ", find_path(graph))
    print("Part 2: ", find_path(for_part_2(graph)))


if __name__ == "__main__":
    main()
