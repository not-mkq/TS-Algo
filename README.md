

# TS-Algo  

A temporal sequence-based high-entropy optimization algorithm (Python implementation).  

## Usage (For Linux Users)  

### Clone This Repository  
```bash
git clone https://github.com/not-mkq/TS-Algo.git
cd TS-Algo
```  

### Set Up a Virtual Environment  
```bash
python -m venv TS-Algo-VENV
```  

Activate the virtual environment based on your shell:  
```bash
source TS-Algo-VENV/bin/activate.fish  # For Fish shell  
source TS-Algo-VENV/bin/activate       # For Bash shell  
source TS-Algo-VENV/bin/activate.csh   # For Csh shell  
```  

### Install Dependencies  
```bash
pip install -r requirements.txt
```  

### Run the Optimization  
```bash
python A<nn>_<xx>.py --csv Exp_data/A<nn>_data.csv <N> <N> <N> <N> <N>
```  
Example output:  
```bash
$ python A66_MB.py --csv Exp_data/A66_data.csv 4 4 3 3 3
4,69.16,102.74,103.41,127.95,
8,69.16,87.05,100.41,102.18,102.74,
12,69.16,87.05,94.8,100.41,102.18,
16,69.16,87.05,94.8,96.06,100.41,
...
```  
- The first column represents the number of data points used for optimization.  
- The remaining columns show the best result, second-best result, and so on.  

### Parameters  

#### `nn`  
- Specifies the dataset:  
  - `55`: A55 system (Exp_data/A55_data.csv)  
  - `66`: A66 system (Exp_data/A66_data.csv)  
- You can modify the `elements` variable in `A<nn>_<xx>.py` to match your dataset.  

#### `xx`  
Defines the exploration and prediction methods:  
- **First character (`x`)**: Exploration method  
- **Second character (`x`)**: Prediction method  

Available options:  
- `A`: Ignores the loci of genes  
- `B`: Considers the loci of genes  
- `M`: A mixed approach combining `A` and `B` (see `lib/iter_gmap.py`)  
- `Random`: A baseline random optimization method  

#### `N`  
Each `N` represents a batch containing `4 × 3 = 12` data points (as defined in `lib/arg_parser.py`). It is parsed into a tuple `(N, 4-N, 3)`, where:  
- `N`: Number of data points explored in each cycle  
- `4-N`: Number of data points predicted  
- The process repeats three times  
