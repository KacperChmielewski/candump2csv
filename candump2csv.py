#!/usr/bin/env python3

import can
import cantools
import csv
import os

output_dir = "."
output_dir = "output"


# Function to parse each line of the dump.log file
def parse_log_line(line):
    parts = line.strip().split()
    if len(parts) < 3:
        return None, None, None  # Skip lines without enough parts
    timestamp = float(parts[0][1:-1])  # Extract timestamp without parentheses
    can_id_part = parts[2].split('#')
    if len(can_id_part) != 2:
        return None, None, None  # Skip lines without valid CAN ID format
    can_id = int(can_id_part[0], 16)  # Extract hexadecimal part before '#'
    if can_id_part[1] == "R":
        return None, None, None  # Skip request frames
    data = bytes.fromhex(can_id_part[1])
    return timestamp, can_id, data


# Function to generate CSV for each frame type
def generate_csv_for_frame(db, frame_id, frame_messages):
    message = db.get_message_by_frame_id(frame_id)
    filename = f"{output_dir}/frame_{message.name}.csv"
    if len(message.signals) == 0:
        return
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp'] + [signal.name for signal in message.signals])
        for message in frame_messages:
            decoded_data = db.decode_message(message.arbitration_id, message.data)
            writer.writerow([message.timestamp] + [value for _, value in decoded_data.items()])


def process_candump(dbc_file: str, candump_log_file: str):
    # Load DBC file
    database = cantools.database.load_file(dbc_file)

    # Load candump file
    with open(candump_log_file, 'r') as f:
        lines = f.readlines()

    parsed_messages = []
    lines_amount = len(lines)
    current_line = 0
    for line in lines:
        current_line += 1
        print(f"Processing line: {current_line} out of {lines_amount} ({current_line / lines_amount * 100:6.2f}%)")
        timestamp, can_id, data = parse_log_line(line)
        try:
            parsed_messages.append(can.Message(timestamp=timestamp, arbitration_id=can_id, data=data))
        except KeyError:
            pass

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frames_amount = len(database._frame_id_to_message)
    current_frame = 0
    for frame_id in database._frame_id_to_message:
        current_frame += 1
        print(f"Processing frame: {current_frame} out of {frames_amount} ({current_frame / frames_amount * 100:6.2f}%)")
        frame_messages = [message for message in parsed_messages if message.arbitration_id == frame_id]
        if frame_messages:
            generate_csv_for_frame(database, frame_id, frame_messages)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <dbc_file> <candump_log_file>")

        sys.exit(1)

    dbc = sys.argv[1]
    candump = sys.argv[2]

    process_candump(dbc, candump)
