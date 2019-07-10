#!/usr/bin/env python3

import json
import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import prettyprint, prettyprint_summary
from tgs.objects import Animation

parser = argparse.ArgumentParser(
    description="Pretty prints a lottie file"
)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "--summary",
    "-s",
    action="store_true",
    help="Just show a short summary"
)

ns = parser.parse_args()

an = Animation.load(json.load(open(ns.infile)))

if ns.summary:
    prettyprint_summary(an)
else:
    prettyprint(an)

