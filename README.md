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

## Problems Installing (Mac)

For some reason, there can be problems installing scikit-learn (necessary for pyabc) for certain versions of python from pip on MacBooks with the new M1 chip. One possible way around this is to use the Conda version of scikit-learn, which should work. This requires you to install Miniconda from here https://docs.conda.io/en/latest/miniconda.html and then follow these instructions:

```
conda create --name FitModelsData
conda activate FitModelsData
conda install scikit-learn
pip install git+https://github.com/icb-dcm/pyabc.git
conda install -c astropy corner
pip install ipython jupyter seaborn
```

## Running the Notebook

Once you have installed the packages above and activated the FitModelsDataEnv environment, you can start running the Jupyter Notebook by typing ```jupyter notebook``` in the Terminal and clicking on FitModelsDataABC.ipynb
