# Weather Data Analysis with Apache Beam

A demonstration Apache Beam pipeline that performs weather data analysis using core data processing concepts including transformations, aggregations, and parallel processing.

## 📋 Overview

This lab demonstrates a complete Apache Beam pipeline that:
- Reads and parses weather observation data
- Performs multiple parallel analyses
- Aggregates data by different dimensions (station, date, temperature ranges)
- Calculates statistical metrics


## 🔧 Prerequisites

- Python 3.9+
- Apache Beam 2.68.0

## 📦 Installation

```bash
# Create virtual environment (recommended)
python -m venv beam_env
source beam_env/bin/activate  # On Windows: beam_env\Scripts\activate

# Install Apache Beam
pip install apache-beam==2.68.0

# Or with Conda
conda install -c conda-forge apache-beam
```

## 🚀 Running the Pipeline

```bash
python weather_analysis_beam.py
```

## 📊 Pipeline Architecture

```
Sample Data
    ↓
Parse & Filter
    ↓
    ├─→ Analysis 1: Average Temp by Station
    ├─→ Analysis 2: Average Temp by Date
    ├─→ Analysis 3: Temperature Extremes (Min/Max/Avg)
    └─→ Analysis 4: Temperature Distribution
```

## 🔍 Pipeline Components

### 1. Data Ingestion
```python
beam.Create(sample_data)  # Creates PCollection from in-memory data
```

### 2. Data Parsing
```python
beam.Map(parse_weather_line)  # Transforms CSV to dictionaries
beam.Filter(lambda x: x is not None)  # Removes invalid records
```

### 3. Analysis Branches

#### Analysis 1: Average Temperature by Station
- **Transforms**: Map → GroupByKey → Map
- **Output**: Station-wise temperature averages

#### Analysis 2: Average Temperature by Date
- **Transforms**: Map → GroupByKey → Map
- **Output**: Date-wise temperature averages

#### Analysis 3: Temperature Extremes
- **Transforms**: Map → CombineGlobally(Custom CombineFn)
- **Output**: Min, Max, Average, and Count of all readings

#### Analysis 4: Temperature Distribution
- **Transforms**: Map → CombinePerKey
- **Output**: Count of readings per temperature range

## 📈 Sample Output

```


--- Analysis 1: Average Temperature by Station ---
Station STATION_001: Avg Temp = 16.10°C, Readings = 4
Station STATION_002: Avg Temp = 12.50°C, Readings = 3
Station STATION_003: Avg Temp = 25.30°C, Readings = 3

--- Analysis 2: Average Temperature by Date ---
Date 2025-09-01: Avg Temp = 17.93°C, Readings = 4
Date 2025-09-02: Avg Temp = 17.50°C, Readings = 3
Date 2025-09-03: Avg Temp = 18.50°C, Readings = 3

--- Analysis 3: Extreme Temperatures ---
Max: 26.10°C, Min: 11.50°C, Avg: 18.03°C, Total Readings: 10

--- Analysis 4: Temperature Distribution ---
Mild (10-20°C): 7 readings
Warm (20-30°C): 3 readings
```

## 🧩 Key Apache Beam Concepts Demonstrated

### PTransforms
| Transform | Purpose | Usage in Lab |
|-----------|---------|--------------|
| `beam.Create` | Create PCollection from in-memory data | Generate sample weather data |
| `beam.Map` | 1:1 transformation | Parse CSV, extract fields, format output |
| `beam.Filter` | Remove elements | Filter out invalid/null records |
| `beam.GroupByKey` | Group by key | Aggregate by station/date |
| `beam.CombineGlobally` | Global aggregation | Calculate overall statistics |
| `beam.CombinePerKey` | Per-key aggregation | Count by temperature range |
| `beam.io.WriteToText` | Write to file sink | Save analysis results |

### Custom CombineFn
```python
class CalculateExtremesCombineFn(beam.CombineFn):
    def create_accumulator(self):
        # Initialize accumulator
        
    def add_input(self, accumulator, element):
        # Add element to accumulator
        
    def merge_accumulators(self, accumulators):
        # Merge multiple accumulators (for parallel processing)
        
    def extract_output(self, accumulator):
        # Extract final result
```



