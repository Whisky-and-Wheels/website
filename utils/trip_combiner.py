#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from dataclasses import dataclass
from functools import reduce
from typing import Text

import yaml


@dataclass
class Time:
    """Time data handler"""

    time: Text

    def __post_init__(self):
        self.day = 0
        tmp = self.time.split("-")
        if len(tmp) > 1:
            self.day = int(tmp[0])
            tmp = tmp[1]
        else:
            tmp = tmp[0]
        self.hour, self.min, self.sec = [int(x) for x in tmp.split(":")]

    def __repr__(self):
        return self.from_data(self.day, self.hour, self.min, self.sec)

    def __str__(self):
        return self.__repr__()

    @property
    def all_sec(self) -> float:
        """Convert to seconds"""
        return self.sec + self.min * 60 + self.hour * 3600 + self.day * 24 * 3600

    @staticmethod
    def from_data(day: int, hour: int, minute: int, sec: int) -> Text:
        """Convert integer data to text"""
        if day > 0:
            return f"{day}-{hour:02d}:{minute:02d}:{sec:02d}"
        return f"{hour:02d}:{minute:02d}:{sec:02d}"

    def __add__(self, other):
        total_sec = self.sec + other.sec
        remaining_sec = total_sec % 60
        total_min = self.min + other.min + (total_sec // 60)
        remaining_min = total_min % 60
        total_hour = self.hour + other.hour + (total_min // 60)
        remaining_hour = total_hour % 24
        total_day = self.day + other.day + (total_hour // 24)

        return Time(
            self.from_data(total_day, remaining_hour, remaining_min, remaining_sec)
        )


def average_speed(distance: float, duration: Time) -> float:
    """
    Compute average speed from distance and duration

    Args:
        distance (`float`): distance in km
        duration (`Time`): duration

    Returns:
        float: average speed in km/h
    """
    return 3600 * distance / duration.all_sec


def main(args):
    """Main function"""

    index_md = os.path.join(args.TRIPPATH, "index.md")
    trip_files = os.listdir(args.TRIPPATH)

    index = {}
    start_loc, end_loc = 0, 0
    if os.path.isfile(index_md):
        with open(index_md, "r") as f:
            index_file = f.read()
        start_loc = index_file.find("---\n") + len("---\n")
        end_loc = index_file.find("\n---")
        index = yaml.safe_load(index_file[start_loc:end_loc])

    index.update(
        {
            "kilometres": 0.0,
            "average_speed": 0.0,
            "total_duration": Time("0:0:0"),
            "ascent": 0.0,
            "descent": 0.0,
        }
    )
    number_of_trips = 0
    for trip in (os.path.join(args.TRIPPATH, x) for x in trip_files):
        if trip == index_md:
            continue

        with open(trip, "r") as f:
            content = f.read()
        begin = content.find("---\n") + len("---\n")
        end = content.find("\n---")
        content = yaml.safe_load(content[begin:end])

        current_distance = content.get("kilometres", 0.0)
        current_duration = Time(content.get("total_duration", "0:0:0"))

        index["kilometres"] += current_distance + content.get("sidetrip_km", 0.0)
        index["ascent"] += content.get("ascent", 0.0)
        index["descent"] += content.get("descent", 0.0)
        index["average_speed"] += content.get(
            "average_speed", average_speed(current_distance, current_duration)
        )
        number_of_trips += 1

        index["total_duration"] = reduce(
            lambda a, b: a + b,
            [
                index["total_duration"],
                current_duration,
                Time(content.get("sidetrip_duration", "0:0:0")),
            ],
        )

    index["kilometres"] = int(index["kilometres"])
    index["ascent"] = int(index["ascent"])
    index["descent"] = int(index["descent"])
    index["total_duration"] = str(index["total_duration"])
    index["average_speed"] = round(index["average_speed"] / number_of_trips, 1)
    content = yaml.dump(index)

    if end_loc == 0:
        include = ""
    else:
        include = index_file[end_loc + len("---\n") + 1 :]

    with open(index_md, "w") as f:
        f.write("---\n" + content + "---\n" + include)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Combine trip statistics")

    parameters = parser.add_argument_group("Trip details")
    parameters.add_argument(
        "--trip-path",
        "-tp",
        type=str,
        help="Absolute path of the trip",
        dest="TRIPPATH",
        required=True,
    )

    args = parser.parse_args()

    args.TRIPPATH = os.path.abspath(args.TRIPPATH)

    main(args)
