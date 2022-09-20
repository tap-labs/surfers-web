# Surfers Lookout

Writing this as want to create a Surf report web site, including Live CAMs without all the bloat and privacy issues in the commercial crop dominating the internet. This has been motiviated by the fact that all local sites here in Sydney now have enforced a charge model for what is typically low quality reporting with CAM feeds from public cameras.

## Current features
- Map based navigation
- location search bar with autocomplete
- surf cams 
- Persistence via MySQL or sqlite
- Support for k8s service binding
- Weather alert ticker from BOM RSS feeds
- Spot based current weather forecast from BOM API

## Being worked on
- Site specific information  to add **(done this kind of with willyweather widgets but needs to be better)**
    - Weather
    - Tide
    - Wave buoy informtion


## To Do
- Add authentication to bring user context to the app
- Add chat forum, location aligned (and general chat?)
- Add information into panels to allow users to customise their own page layouts
- Enable session context to be externalised to Redis (flask-session module maybe?)
- Add admin screen to allow locations to be added/managed via web UI

## The Website ingredients
*Language:*   **Python** (initially), minimum version 3.10

### Modules in use
- [Flask](https://flask.palletsprojects.com/) - super easy lightweight web framework for Python
- [SQLAchemy](https://www.sqlalchemy.org/) - Python database ORM with *Flask-SQLAchemy*
- [Chart.js](https://www.chartjs.org/): *(javascript)* Chart.js provides the rendered graphs capability
- [Videojs](https://videojs.com/): *(javascript)* CAM footage player is provided by videojs
- [jquery](https://jquery.com/) *(javascript)* Various features including banner support

### Embedded web widgets
- Willy Weather https://www.willyweather.com.au/widget/create.html
- Google Maps for embbedded location maps


**Currently Under Investigation**
- Various Wave Buoy feeds for swell and tidal information
- OSS HTML movable element modules vs self defined  


