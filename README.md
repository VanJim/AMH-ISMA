# AMH–ISMA Data and Plotting Code

This repository contains the Python scripts and experimental data used to generate the main results in the manuscript:

> W. Zhang, Z.C. Ong, Z. Pan, "Development and Validation of an AMH–ISMA System for High-Efficiency Impact Synchronous Modal Analysis", Journal of Vibration Engineering & Technologies, 2025.

All scripts are written in Python 3 and can be run on a standard PC. The experimental data are embedded directly in the `.py` files as arrays, so no separate data files are required.

## Contents

All scripts are self-contained and include both the experimental data (as Python arrays) and the plotting code used to generate the figures in the paper.

- `calibration/AMH_bluetip.py`  
  Calibration data and plotting code for the blue hammer tip (500 force–speed data pairs).

- `calibration/AMH_whitetip.py`  
  Calibration data and plotting code for the white hammer tip (300 force–speed data pairs).

- `AMH_ISMA/AMH-ISMA 4averaged20Hz.py`  
  AMH–ISMA response data and plotting code for 4 phase-controlled impacts at 20 Hz.

- `AMH_ISMA/AMH-ISMA 4averaged30Hz.py`  
  AMH–ISMA response data and plotting code for 4 phase-controlled impacts at 30 Hz.

- `AMH_ISMA/AMH-ISMA 8averaged 20Hz.py`  
  AMH–ISMA response data and plotting code for 8 phase-controlled impacts at 20 Hz.

- `AMH_ISMA/AMH-ISMA 8averaged30Hz.py`  
  AMH–ISMA response data and plotting code for 8 phase-controlled impacts at 30 Hz.

- `AMH_ISMA/ISMA 1averaged20Hz.py`  
  Single-impact ISMA response data and plotting code at 20 Hz.

- `AMH_ISMA/ISMA 1averaged30Hz.py`  
  Single-impact ISMA response data and plotting code at 30 Hz.

- `AMH_ISMA/EMA.py`  
  Experimental data and plotting code for the benchmark EMA test on the rotor rig.

- `Random_ISMA/Random ISMA 30averages 20Hz.py`  
  Random-ISMA response data and plotting code for 30 averaged impacts at 20 Hz.

- `Random_ISMA/Random ISMA 30averages 30Hz.py`  
  Random-ISMA response data and plotting code for 30 averaged impacts at 30 Hz.


## Requirements

- Python 3.x  
- Standard scientific Python stack (e.g. `numpy`, `matplotlib`)

## Usage

1. Clone or download this repository.
2. Open a terminal in the repository folder.
3. Run any script with Python to reproduce the corresponding figures in the paper, for example:

   ```bash
   python "AMH-ISMA 8averaged30Hz.py"
