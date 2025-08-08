# ELAT (edX Learning Analytics Tool) - Modifications for KU Leuven MOOC Data

This repository contains a modified version of the ELAT tool, customized to process and analyze the specific data format from the KU Leuven MOOCs on the edX platform for my Master's thesis.

**Original Tool Source:** https://github.com/mvallet91/ELAT-Workbench

---

## Summary of Modifications

Two primary modifications were made to the original source code to ensure correct data parsing and visualization rendering. A custom pre-processing script was also developed to handle non-unique video metadata.

### 1. Core Tool Modifications

#### File 1: `index.js`
* **Purpose:** To correct the log file parsing incompatibility with the KU Leuven dataset.
* **Change:** In the `unzipAndChunkLogfile` function, the hardcoded string search used to identify the start of a JSON event line was changed from `{"username":` to `{"name":`. This was necessary because the KU Leuven logs begin with the `name` key.

#### File 2: `graphProcessing.js`
* **Purpose:** To resolve a critical rendering error that prevented visualizations from being generated.
* **Change:** In the `drawChartJS` function, the call to an internal function `drawBoxChart` was commented out. This function was causing the script to fail due to an outdated JavaScript library dependency, and it was not essential for the primary analyses in this thesis.

### 2. Custom Pre-processing Script

In addition to the modifications above, a separate custom script was developed to address an issue with the "video interaction" chart.

* **Script Name:** `preprocessor.py`
* **Purpose:** To resolve an issue where non-unique video names (e.g., "Video") caused the interaction graph nodes to collapse.
* **Process:** The script parses the course's original XML structure to extract the unique `client_video_id` for each video. It then systematically replaces the generic `display_name` field in the course's metadata JSON file with this unique ID, allowing the visualization to render correctly.
