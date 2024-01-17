#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import copy
import os
from dataclasses import dataclass
from functools import reduce
from typing import Text, Union

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


_meta = {
    "kilometres": 0.0,
    "average_speed": 0.0,
    "total_duration": "0:0:0",
    "ascent": 0.0,
    "descent": 0.0,
    "sidetrip_km": 0.0,
    "sidetrip_duration": "0:0:0",
}

_types = {
    "kilometres": int,
    "average_speed": lambda x: round(x, 1),
    "ascent": int,
    "descent": int,
    "total_duration": str,
    "sidetrip_duration": str,
    "sidetrip_km": int,
}


@dataclass
class Trip:

    filename: Text

    def __post_init__(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                content = f.read()
            start_loc = content.find("---\n")
            start_loc += (start_loc >= 0) * len("---\n")
            end_loc = content.find("\n---")
            if start_loc >= 0 and end_loc >= 0:
                self.meta = yaml.safe_load(content[start_loc:end_loc])
                self.content = content[end_loc + len("---\n") + 1 :]
        else:
            self.meta = {**_meta}
            self.content = "Add your story here..."

    def get(self, key: Text) -> Union[Time, float]:
        """Retreive metadata"""
        if "duration" in key:
            time = self.meta.get(key, "0:0:0")
            if isinstance(time, Time):
                return time
            return Time(time)
        return self.meta.get(key, 0.0)

    def update(self, **kwargs) -> None:
        """Update metadata"""
        self.meta.update(kwargs)

    def write(self):
        """write to a file"""
        meta = copy.deepcopy(self.meta)
        for key, item in _types.items():
            meta[key] = item(meta.get(key, _meta[key]))
        with open(self.filename, "w") as f:
            f.write("---\n" + yaml.dump(meta) + "---\n" + self.content)


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

    index_md = Trip(os.path.join(args.TRIPPATH, "index.md"))
    index_md.update(**_meta)
    trip_files = [
        os.path.join(args.TRIPPATH, x)
        for x in os.listdir(args.TRIPPATH)
        if os.path.join(args.TRIPPATH, x) != index_md.filename and x.endswith(".md")
    ]

    number_of_trips = len(trip_files)
    for trip in (os.path.join(args.TRIPPATH, x) for x in trip_files):
        if trip == index_md.filename:
            continue

        current_trip = Trip(trip)

        current_distance = current_trip.get("kilometres")
        current_duration = current_trip.get("total_duration")

        index_md.meta["kilometres"] += current_distance + current_trip.get("sidetrip_km")
        index_md.meta["ascent"] += current_trip.get("ascent")
        index_md.meta["descent"] += current_trip.get("descent")

        if args.UPDATESUB:
            current_trip.update(
                average_speed=average_speed(current_distance, current_duration)
            )
            current_trip.write()

        index_md.meta["average_speed"] += (
            current_trip.get("average_speed") / number_of_trips
        )

        index_md.meta["total_duration"] = reduce(
            lambda a, b: a + b,
            [
                index_md.get("total_duration"),
                current_duration,
                current_trip.get("sidetrip_duration"),
            ],
        )

    index_md.write()


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
    parameters.add_argument(
        "--update-subtrips",
        "-u",
        action="store_true",
        default=False,
        help="Update subtrips.",
        dest="UPDATESUB",
    )

    args = parser.parse_args()

    args.TRIPPATH = os.path.abspath(args.TRIPPATH)

    main(args)
