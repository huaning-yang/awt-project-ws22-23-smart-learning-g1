# # Read this xml file C:\Users\Oscar\Downloads\2022-11-02_FOKUS_AWT_CompetencyExtraction_WB_Brandenburg_re-encoded - Kopie.xml
# import xml.etree.ElementTree as ET
# import os
# import xml.etree.ElementTree as ET

# tree = ET.parse('C:/Users/Oscar/Downloads/2022-11-02_FOKUS_AWT_CompetencyExtraction_WB_Brandenburg_re-encoded - Kopie.xml')
# root = tree.getroot()

# # Returns a list of unique values from the A_CITY attribute in the xml file


# print(get_unique_city_values())

from bs4 import BeautifulSoup
 
 
# Reading the data inside the xml
# file to a variable under the name
# data
with open('C:/Users/Oscar/Downloads/2022-11-02_FOKUS_AWT_CompetencyExtraction_WB_Brandenburg_re-encoded - Kopie.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag
# `unique`
b_unique = Bs_data.find_all('A_CITY')

def get_unique_city_values():
    unique_city_values = []
    for child in b_unique:
        if child not in unique_city_values:
            unique_city_values.append(child)
    return unique_city_values
 
print(get_unique_city_values())