
import sys

import princeton_scraper_seas_faculty.output


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"


# noinspection PyBroadException
if __name__ == "__main__":

    is_fast = False
    is_csv = False

    # "parse" command line parameter
    # NOTE: should be a real command line tool

    if len(sys.argv) > 0:
        if "--csv" in sys.argv:
            is_csv = True

        if "--fast" in sys.argv:
            is_fast = True

    # output selected format

    output = None
    if is_csv:
        output = princeton_scraper_seas_faculty.output.csv_output(fast=is_fast)
    else:
        output = princeton_scraper_seas_faculty.output.json_output(fast=is_fast)

    if output is None:
        sys.exit(1)
    else:
        print(output)
        sys.exit(0)
