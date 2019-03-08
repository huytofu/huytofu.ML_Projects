# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ListingItem(scrapy.Item):
# define the fields for your item here like:
# name = scrapy.Field()
	ListingTitle = scrapy.Field()
	RentalRate = scrapy.Field()
	NumBeds = scrapy.Field()
	NumBaths = scrapy.Field()
	Area_Sqft = scrapy.Field()
	Price_psf = scrapy.Field()
	Furnishing = scrapy.Field()
	Lease = scrapy.Field()
	Keys_On_Hand = scrapy.Field()
	Facing = scrapy.Field()
	Pets = scrapy.Field()
	Ethnic = scrapy.Field()
	Floor = scrapy.Field()
	District = scrapy.Field()
	Amenities = scrapy.Field()
	Description = scrapy.Field()
	Url = scrapy.Field()
	pass
	