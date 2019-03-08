# This project involves exploring the details about SG rental properties and perform some fun predictions/filtering on the data
### The data comes from scraping data off the www.99.co website

### There is a Flaskapp on top of the conventional Ipython Notebook to consolidate the project into a runable program
### The app utilizes already cleaned dataset. To check out the data cleaning and perparation process please refer to the "Cleaning Dataset" notebook

### There are 3 sections to this project
  1. Exploratory Data Analysis of the data using Seaborn & Dash
  2. Predicting Rental Rate of a Hypothetical Property proposed by the user
  3. Filtering Similar Properties to one proposed by the user based on his/her specified importance of individual features
  
### Features of a property includes:
  1. RentalRate (not available for section 2)
  2. Area_Sqft
  3. Price_psf
  4. Number of bedrooms
  5. Furnishing
  6. District of Location
  7. Amenities
  ...
  
### The Flaskapp are deployed in 2 ways: locally and on the hosting site Heroku (https://sg-property-99co.herokuapp.com/)
### There are some differences to the two versions
  1. Due to Heroku's low memory policy, the hosted version only can plot a fraction of the data (chosen by user) in its interactive scatter plot
  2. The hosted version has a Scatter Plot Preparation Phase with occasional alert messages to comply with Heroku's 30 seconds timeout policy
  3. There is no choice for building up models using Pyspark in the hosted version (also due to low memory policy of Heroku)
  4. Interactive Barcharts and Scatter Plot are viewed separately in the hosted version