# FitModelsData
Accompaniment to the "Fitting Models to Data" session at the ISEEC workshop 2022

## Installation

This session is compatible with Python 3.7 or above. It requires numpy (basic maths functions), scipy (special maths functions), pandas (dataframes manipulation), pyabc (Approximate Bayesian Computation), jupyter (interactive notebook), matplotlib (plotting), arviz (Bayesian plotting), corner (Bayesian plotting)

The package can be installed directly from a local copy of the Github repo. I recommend creating a virtual environment to run this notebook in, using venv, and pip to install the dependencies (conda can also be used) from the Terminal:

```
git clone https://github.com/CalumGabbutt/FitModelsData.git
cd FitModelsData
python3 -m venv FitModelsDataEnv
source FitModelsDataEnv/bin/activate
pip install -r requirements.txt
```

## Running the Notebook

Once you have installed the packages above and activated the FitModelsDataEnv environment, you can start running the Jupyter Notebook by typing ```jupyter notebook``` in the Terminal
