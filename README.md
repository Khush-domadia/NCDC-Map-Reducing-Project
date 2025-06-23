# Big Data Weather Analysis Project: NCDC Temperature Data Processing

## Project Overview

This project implements a comprehensive big data analysis pipeline for processing National Climatic Data Center (NCDC) weather records using Apache Hadoop ecosystem tools. The project demonstrates end-to-end big data processing from raw weather data extraction to statistical analysis using MapReduce, Pig, and Hive technologies. The system processes historical temperature data spanning from 1930 onwards to extract meaningful insights about temperature patterns and trends.

## Project Architecture

### Three-Part Analysis Pipeline

The project follows a structured three-part approach to big data analysis:

1. **Data Extraction**: Python MRJob application for temperature data extraction from NCDC records
2. **Statistical Analysis**: Pig-based computation of minimum and maximum temperatures per year
3. **Aggregation Analysis**: Hive-based calculation of average temperatures per year

### Technology Stack

- **Hadoop Distributed File System (HDFS)**: Distributed storage for large-scale weather datasets
- **Python MRJob**: MapReduce framework for data processing and extraction
- **Apache Pig**: High-level platform for analyzing large datasets with simple scripting
- **Apache Hive**: Data warehouse software for querying and managing large datasets
- **WinSCP**: Secure file transfer protocol client for file management
- **PuTTY**: SSH and telnet client for remote command execution

## Data Source and Format

### Dataset Information
- **Source**: National Climatic Data Center (NCDC) weather records
- **Format**: Fixed-width format text files with compressed (.gz) archives
- **Time Range**: Historical weather data from 1930 onwards
- **Data Volume**: Multiple compressed files requiring distributed processing

### Data Schema
The NCDC records follow a specific fixed-width format where:
- **Year**: Positions 15-19 in each record
- **Temperature**: Positions 87-92 in each record
- **Quality Indicator**: Position 92 for data validation
- **Missing Data Indicator**: 9999 represents missing temperature readings

## Implementation Details

### Part 1: Python MRJob Temperature Extractor

The core data extraction component (`temp_extractor.py`) implements a MapReduce job with the following features:

#### Mapper Functionality
```python
def mapper(self, _, line):
    # Parse fixed-width NCDC records
    year = line[15:19]
    temp_str = line[87:92]
    quality = line[92]
```

**Key Processing Steps**:
- Validates record length (minimum 93 characters)
- Extracts year and temperature from fixed positions
- Handles positive temperature indicators (removes leading '+')
- Filters out missing data (temperature != 9999)
- Quality control filtering (accepts quality codes: 0, 1, 4, 5, 9)

#### Reducer Functionality
The reducer processes year-temperature pairs and outputs clean data in "year temperature" format.

#### Output Protocol
Uses `RawValueProtocol` to prevent automatic quote addition in output formatting.

### Part 2: Pig Statistical Analysis

The Pig script (`year_minmax.pig`) performs statistical aggregation:

```pig
raw_data = LOAD '/user/student8/input/year_temp_output.txt' 
            USING PigStorage(' ') 
            AS (year: chararray, temp: int);
grouped_data = GROUP raw_data BY year;
min_max_temp = FOREACH grouped_data GENERATE 
                 group AS year, 
                 MIN(raw_data.temp) AS min_temp, 
                 MAX(raw_data.temp) AS max_temp;
```

**Analysis Capabilities**:
- Groups temperature data by year
- Calculates minimum temperature per year
- Calculates maximum temperature per year
- Outputs results in CSV format

### Part 3: Hive Data Warehousing

The Hive analysis creates a structured data warehouse approach:

```sql
CREATE TABLE year_temp (
    year STRING,
    temperature INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
STORED AS TEXTFILE;
```

**Analytical Queries**:
- Loads processed data into Hive tables
- Calculates average temperatures per year using SQL-like syntax
- Provides ordered results for temporal analysis

## Project Structure

```
├── temp_extractor.py              # MRJob temperature extraction script
├── The-Project-report.docx        # Comprehensive project documentation
├── year_temp_output.txt          # Processed temperature data output
├── year_minmax.pig              # Pig script for min/max analysis
├── NewProjectData.zip           # Compressed NCDC source data
└── README.md                    # This documentation
```

## Hadoop Cluster Setup and Execution

### Environment Configuration
- **Cluster URL**: 134.154.190.204
- **User Directory**: /user/student8/
- **File Management**: WinSCP for secure file transfers
- **Command Interface**: PuTTY for SSH-based Hadoop operations

### HDFS Directory Structure
```
/user/student8/
├── ncdc_input/          # Input directory for compressed NCDC files
├── ncdc_output/         # MRJob processing output
├── input/               # Pig input directory
└── output/              # Final analysis results
```

### Execution Workflow

#### 1. Data Preparation
```bash
# Create HDFS input directory
hdfs dfs -mkdir -p /user/student8/ncdc_input

# Upload compressed data files
hdfs dfs -put *.gz /user/student8/ncdc_input/
```

#### 2. MRJob Execution
```bash
# Run Python MRJob application
python temp_extractor.py -r hadoop \
  hdfs:///user/student8/ncdc_input/* \
  --output-dir hdfs:///user/student8/ncdc_output
```

#### 3. Data Consolidation
```bash
# Merge distributed output files
hdfs dfs -getmerge /user/student8/ncdc_output/ year_temp_output.txt
```

#### 4. Pig Analysis
```bash
# Execute Pig script
pig year_minmax.pig
```

#### 5. Hive Analysis
```bash
# Initialize Hive metastore
schematool -dbType derby -initSchema

# Start Hive and execute queries
hive
```

## Data Processing Results

### Sample Output Format
The processed data follows a consistent "year temperature" format:
```
1930 61
1930 28
1930 22
1930 50
...
```

### Data Volume and Coverage
- **Temporal Span**: Historical data from 1930 onwards
- **Processing Scale**: Thousands of temperature readings per year
- **Geographic Coverage**: NCDC weather station network data

### Quality Assurance
- **Missing Data Handling**: Filters out 9999 temperature values
- **Quality Code Validation**: Accepts only verified quality indicators
- **Format Standardization**: Consistent year-temperature output format

## Business Intelligence and Applications

### Analytical Capabilities
- **Temporal Trend Analysis**: Year-over-year temperature patterns
- **Statistical Aggregation**: Min, max, and average temperature calculations
- **Climate Research**: Historical temperature data for climate studies
- **Weather Pattern Recognition**: Long-term meteorological analysis

### Use Cases
- **Climate Change Research**: Historical temperature trend analysis
- **Agricultural Planning**: Temperature-based crop planning insights
- **Energy Management**: Temperature-driven energy consumption forecasting
- **Environmental Monitoring**: Long-term climate pattern assessment

## Technical Requirements

### System Dependencies
- **Hadoop Cluster**: Distributed computing environment
- **Python 2.7+**: MRJob framework compatibility
- **Apache Pig**: Data flow scripting platform
- **Apache Hive**: SQL-on-Hadoop query engine
- **Java Runtime**: Hadoop ecosystem requirement

### Development Tools
- **WinSCP**: Secure file transfer for data management
- **PuTTY**: SSH client for remote cluster access
- **Text Editors**: Script development and configuration

## Performance Characteristics

### Scalability Features
- **Distributed Processing**: Hadoop's distributed computing capabilities
- **Fault Tolerance**: HDFS replication and recovery mechanisms
- **Parallel Execution**: MapReduce parallel processing paradigm
- **Resource Management**: YARN-based resource allocation

### Processing Efficiency
- **Data Locality**: Hadoop's data-local processing optimization
- **Compression Support**: Efficient handling of .gz compressed files
- **Memory Management**: Optimized data structure handling

## Future Enhancements

### Potential Improvements
- **Real-time Processing**: Integration with Apache Kafka for streaming data
- **Advanced Analytics**: Machine learning integration with Spark MLlib
- **Visualization**: Integration with business intelligence tools
- **Data Quality**: Enhanced data validation and cleansing pipelines

### Scalability Expansions
- **Multi-node Clusters**: Expanded Hadoop cluster deployment
- **Cloud Integration**: AWS/Azure Hadoop service integration
- **Automated Workflows**: Apache Airflow workflow orchestration

## Getting Started

### Prerequisites
1. Access to Hadoop cluster environment
2. WinSCP installed for file management
3. PuTTY configured for SSH access
4. Python MRJob library installed

### Quick Start Guide
1. **Clone Repository**: Download project files to local environment
2. **Prepare Data**: Extract and upload NCDC data files using WinSCP
3. **Execute Pipeline**: Run the three-part analysis workflow
4. **Analyze Results**: Review statistical outputs and temperature trends

## License and Usage

This project demonstrates academic and research applications of big data technologies for climate data analysis. The implementation serves as a comprehensive example of Hadoop ecosystem integration for large-scale data processing workflows.

---

**Note**: This project was developed as part of a big data analytics course, demonstrating practical applications of distributed computing technologies for real-world climate data analysis.

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/46181816/17fab19f-f82e-4845-8c8b-c6f7e0acd985/temp_extractor.py
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/46181816/7fdfed8c-7644-460b-b1fa-883607cef4f2/year_temp_output.txt
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/46181816/686db2bc-1e6e-46fa-9d8c-a1caf80c2d0f/The-Project-report.docx
