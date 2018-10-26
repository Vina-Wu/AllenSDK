import sys
import nwb1_reader
import logging
import ipfx.lab_notebook_reader as lab_notebook_reader
import build_nwb2_file
import os
from pynwb import NWBHDF5IO


DEFAULT_NWB1_FILE_NAME ="/allen/aibs/technology/sergeyg/ephys_pipeline/nwb_conversion/nwb1/Npr3-IRES2-CreSst-IRES-FlpOAi65-401243.04.01.01.nwb"



def main():

    """
    Usage:
    $python convert_nwb1_to_nwb2.py NWB1_FILE_NAME
    """
    logging.basicConfig(level="INFO")

    if len(sys.argv) == 1:
        sys.argv.append(DEFAULT_NWB1_FILE_NAME)

    nwb1_file_name = sys.argv[1]
    dir_name = os.path.dirname(nwb1_file_name)
    base_name = os.path.basename(nwb1_file_name)
    file_name, file_extension = os.path.splitext(base_name)
    nwb2_file_name = os.path.join(dir_name, file_name+"_ver2" + file_extension)

    nwb1_data = nwb1_reader.create_nwb_reader(nwb1_file_name)
    notebook = lab_notebook_reader.create_lab_notebook_reader(nwb1_file_name)

    nwb2file = build_nwb2_file.add_time_series(nwb1_data, notebook)
    logging.info("Created nwb2 file")

    with NWBHDF5IO(nwb2_file_name, mode='w') as io:
        io.write(nwb2file)

    logging.info("Saved the nwb2 file")


if __name__ == "__main__": main()