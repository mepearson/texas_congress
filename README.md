# texas_congress
Dash APP for TX Congressional Info
Note: This app is built using Dash 2.0 and dash-bootstrap-components 1.0 [currently in prerelease]

## Files
* README.md = this file that documents the application
* app.py - Dash application python file
* environment.yml - file to create virtual environment in Conda
* requirements.txt = file to create virtual environment with pip
* Procfile - required file for deploying application to Heroku
* assets folder - dash application natively looks here for resources such as css
  * Texas_Congress.ipynb - Jupyter notebook with data processing steps (for reference)
* data folder - directory to store  local data files

## Data preprocessing
### Congressional geometries
* Congressional geospatial data downloaded from 2021 census.gov shapefiles[https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2021&layergroup=Congressional+Districts+%28116%29]
* Shapefile converted to geojson using mapshaper.org
* US geojson converted to geopandas DataFrame
* TX district data extracted using STATEFP == '48'
* TX district information saved as geojson file
```
import geopandas as gpd
congress = 'data/tl_2021_us_cd116.json'
gdf = gpd.read_file(congress)
texas = gdf[gdf.STATEFP == '48']
texas.reset_index(inplace=True)
texas.to_file('texas_congress.geojson', driver='GeoJSON')

```
### US Congress Districts
* Source for district to map links
https://redistricting.capitol.texas.gov/Current-districts#us-congress-section
* Map locations follow pattern wrm.capitol.texas.gov/fyiwebdocs/PDF/congress/dist{district_number}/m1.pdf

## Future Plans
### Member info links
* scrape page to get member names / district / link to personal page
https://www.congress.gov/members?q=%7B%22congress%22%3A%22117%22%2C%22member-state%22%3A%22Texas%22%7D
