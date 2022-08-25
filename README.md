# Surf Lookout

Looking at the viability of creating a Surf report web site, including Live CAMs. This has been motiviated by the fact that all local sites here in Sydney now have enforced a charge model for what is typically low quality reporting with CAM feeds from public cameras.


## To Do
- Add authentication to bring user context to the app
- Site specific information  to add
    - Weather
    - Tide
    - Wave buoy informtion
- Add chat forum, location aligned (and general chat?)
- Add information into panels to allow users to customise their own page layouts
- Enable session context to be externalised to Redis (flask-session module maybe?)
- Add map based navigation
- Add admin screen to allow locations to be added/managed via web UI


## The Website ingredients
*Language:*   **Python** (initially), minimum version 3.10

### Modules in use
- [Flask](https://flask.palletsprojects.com/) - super easy lightweight web framework for Python
- [SQLAchemy](https://www.sqlalchemy.org/) - Python database ORM with *Flask-SQLAchemy*
- [Chart.js](https://www.chartjs.org/): *(javascript)* Chart.js provides the rendered graphs capability
- [Videojs](https://videojs.com/): *(javascript)* CAM footage player is provided by videojs

### Embedded web widgets

**Currently Under Investigation
- Google Maps for embbedded location maps
- Windguru / weatherwidget.io for weather information (also looking at self made options)
- Various Wave Buoy feeds for swell and tidal information
- OSS HTML movable element modules vs self defined  


