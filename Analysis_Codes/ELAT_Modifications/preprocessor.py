# ==============================================================================
# Python Script for Pre-processing edX Course Structure Metadata
#
# This script addresses an issue where non-unique video display names (e.g., "Video")
# in the course_structure.json file cause visualization errors in the ELAT tool.
#
# It parses the original JSON structure, and for each video component, it finds
# the corresponding XML file in the 'video' directory. It then extracts the
# unique 'client_video_id' from the XML and uses it to replace the generic
# 'display_name' in the JSON metadata.
#
# Author: Ziyun Ke
# Date: August 2025
# ==============================================================================

import json
import os
import xml.etree.ElementTree as ET

def process_json(input_path, output_path, video_dir):
    """
    Reads a course structure JSON, updates video display names with unique IDs
    from corresponding XML files, and writes the modified structure to a new file.
    """
    # Read the original JSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Iterate over all top-level keys in the JSON data
    for key in list(data.keys()):
        # Split the key to get the component ID
        key_parts = key.split('@')
        if len(key_parts) < 3:
            print(f"Warning: Skipping malformed key {key}")
            continue
            
        item_id = key_parts[2]
        item_data = data[key]
        
        # Check if the component is a video
        if item_data.get('category') == 'video':
            # Construct the path to the corresponding XML file
            xml_path = os.path.join(video_dir, f"{item_id}.xml")
            
            # Verify that the XML file exists
            if not os.path.isfile(xml_path):
                raise FileNotFoundError(f"Could not find the corresponding XML file for video ID {item_id}: {xml_path}")
            
            # Parse the XML file to find the unique video ID
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                # The unique ID is typically in the 'client_video_id' attribute of the first child
                video_id = root[0].attrib.get('client_video_id')
                
                if not video_id:
                    raise ValueError(f"Missing 'client_video_id' attribute in XML file: {xml_path}")
                
                # Clean the ID by removing potential file extensions
                video_id = video_id.removesuffix('.mp4')
                video_id = video_id.removesuffix('.mp')
                video_id = video_id.removesuffix('.m')
                
                # Update the metadata in the JSON data
                # Replace the generic display_name with the unique ID
                item_data['metadata']['display_name'] = video_id
            except ET.ParseError:
                raise ValueError(f"Failed to parse XML file: {xml_path}")
    
    # Write the modified data to a new JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)

if __name__ == "__main__":
    # --- Configuration ---
    # NOTE: This script needs to be run for each course by changing the paths.
    # Path to the original course structure JSON file
    input_json = "EUROGOVx/KULeuvenX-EUROGOVx-1T2023-course_structure-prod-analytics.json"
    # Path for the modified output JSON file
    output_json = "EUROGOVx/rep_KULeuvenX-EUROGOVx-1T2023-course_structure-prod-analytics.json"
    # Directory containing the individual video component XML files
    video_folder = "EUROGOVx/video"
    # --- End of Configuration ---
    
    # Execute the processing workflow
    try:
        process_json(input_json, output_json, video_folder)
        print("Processing successful. Results have been saved to:", output_json)
    except Exception as e:
        print("An error occurred during processing:", str(e))
