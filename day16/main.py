from functools import reduce


def read_literal_value(data, version):
    is_last_group = False
    group_number = 1
    packet_end = None
    value = ""
    while not is_last_group:
        start_index = 5 * group_number
        group = data[start_index+1:(start_index+6)]
        if len(group) == 5:
            value += str(data[start_index+2:(start_index+6)])
        group_number += 1
        if int(group[:1]) == 0 or len(group) < 5:
            is_last_group = True
            packet_end = start_index+6
    return [version, packet_end, bin_to_num(value)]

def get_operation_result(packet_id, values):
    result = 0
    if packet_id == 0:
        return sum(values)
    elif packet_id == 1:
        return reduce(lambda x, y: x*y, values)
    elif packet_id == 2:
        return min(values)
    elif packet_id == 3:
        return max(values)
    elif packet_id == 5:
        if values[0] > values[1]:
            return 1
        else:
            return 0
    elif packet_id == 6:
        if values[0] < values[1]:
            return 1
        else:
            return 0
    else:
        if values[0] == values[1]:
            return 1
        else:
            return 0


def read_transmission(data):
    version = bin_to_num(data[:3])
    packet_id = bin_to_num(data[3:6])
    if packet_id == 4:
        return read_literal_value(data, version)
    else:
        length_type_id = int(data[6:7])
        last_index = 0
        values = []
        if length_type_id == 0:
            subpacket_length = bin_to_num(data[7:22])
            is_packet_end = False
            last_index = 22
            last_subpacket_index = 22 + subpacket_length
            while not is_packet_end:
                packet_version, packet_end, packet_value = read_transmission(data[last_index:last_subpacket_index])
                values.append(packet_value)
                version += packet_version
                last_index += packet_end
                if last_index == last_subpacket_index:
                    is_packet_end = True
        else:
            subpacket_count = bin_to_num(data[7:18])
            seen = 0
            last_index = 18
            while seen < subpacket_count:
                packet_version, packet_end, packet_value = read_transmission(data[last_index:])
                values.append(packet_value)
                version += packet_version
                last_index += packet_end
                seen += 1
        return [version, last_index, get_operation_result(packet_id, values)]


def bin_to_num(n):
    return int(n, 2)


def parse_output(filename):
    binary = None
    with open(filename) as fp:
        line = fp.readline()
        while line:
            end_length = len(line) * 4
            binary = bin(int(line, 16))[2:].zfill(end_length)
            line = fp.readline()
    return binary


def main():
    file = parse_output('input.txt')
    version, last_index, values = read_transmission(file)
    print('Part 1: ', version)
    print('Part 2: ', values)


if __name__ == "__main__":
    main()
