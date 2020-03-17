

![Find a campground](static/img/tentative.gif)

#Tentative

> Tentative is a full stack web application that allows would-be campsers to easily view availibility for campground in National Parks.  This site shows availibility and a map of National Parks Campgrounds, and allows a user to link to an available campsite on Recreation.gov.


> Camping, Recreation.gov, National Park Service, NPS, Camping availibility, campground


##Table of Contents

- [Overview](#Overview)
- [Technologies and Stack](#Technologies-and-stack)
- [Features](#Features)


---

Overview
==========
**The Map**  
* Shows all campgrounds in the database (from the recreation.gov api).
* Shows popups for each campground that includes a link to reserve the campground in recreation.gov.
* Changes colors based on availibility of a campground inside a National Park once a user has selected dates and choosen a National Park. 

**Users can:** 
* Select a National Park to see more information about the National Park, its location, and driving directions to the National Park.
* See a list of availibile campgrounds based on date criteria and the name of the National Park. 
* Click on an available campsite to book in recreation.gov.

Technologies and stack
======================
**Backend:**  
SQL, Python, Flask, Flask-SQLAlchemy, Jinja2

**Frontend:**   
JavaScript, jQuery, AJAX, Jinja, HTML5, CSS3, Bootstrap.

**APIs:**   
Recreation.gov API, Recreation.gov availability API, Google Maps for JavaScript, National Park Service


Features
==========
**Find a Campground**  
 Get all of the campgrounds in a National Park from a SQL query. Choose dates to show availability of these campgrounds and zoom in on a map of their location with an AJAX request. Flask app routes AJAX requests to the database and Flask session. 
 
**Map**  
 Google Maps javascript methods to initialize a visual map with all campgrounds. Query database to construct JSON which is supplied to my javascript function to populate the map.
 Used javascript methods to contruct pop-ups for each campground that allows users to view information and link to booking site.

 
**Filtering campsites**  
 Used an SQL query to gather all campgrounds within a National Park.  These are routed to the Recreation.gov availibility database to check availability for each campground. 


---
