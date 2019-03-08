import scrapy
from scrap99dotsg.items import ListingItem
from datetime import datetime
import re

class Scrap99dotsg(scrapy.Spider):
	name = "my_scraper"
	# First Start Url
	start_urls = ["https://www.99.co/singapore/rent"]
	npages = 100
	# This mimics getting the pages using the next button. 
	for i in range(2, npages + 1):
		start_urls.append("https://www.99.co/singapore/rent?page_num="+str(i))
	
	def parse(self, response):
		for href in response.xpath("//a[contains(@class, 'listing-list-item__container_innerWrapper__aYra7')]//@href"):
			# add the scheme, eg http://
			url  = "https://www.99.co" + href.extract() 
			yield scrapy.Request(url, callback=self.parse_dir_contents)	
					
	def parse_dir_contents(self, response):
		item = ListingItem()
		# Getting Listing Title
		item['ListingTitle'] = (response.xpath("//div[contains(@class, 'Listing__titleContainer__5bjht')]/h1[contains(@class, 'Heading__heading__2ncUp')]/descendant::text()").extract()
							   +response.xpath("//div[contains(@class, 'Listing__titleContainer__5bjht')]/a[contains(@class, 'Link__link__2aXf0')]/h1[contains(@class, 'Heading__heading__2ncUp')]/descendant::text()").extract()
							   )[0].strip()
		# Rental Rate 
		item['RentalRate']= response.xpath("//div[contains(@class, 'Listing__rightColumn__1YqJU')]/h3[contains(@class, 'Heading__heading__2ncUp')]/descendant::text()").extract()[0].strip()
		# Getting Listing Attributes
		summary_att = response.xpath("//div[contains(@class, 'Listing__summaryTextContainer__8Oo0l')]/p[contains(@class, 'Text__text__x0JSc') and contains(@class, 'Listing__summaryText__1QR5z')]/descendant::text()").extract()
		att_fields = ['NumBeds','NumBaths','Area_Sqft','Price_psf']
		for j in range(len(summary_att)):	
			item[att_fields[j]] = summary_att[j]
		# Getting Story
		key_fields = response.xpath("//div[contains(@class, 'Listing__keyDetailItem__2sR9y')]/div[contains(@class, 'Tag__tag__1ngVj')]/descendant::text()").extract()
		key_details = response.xpath("//div[contains(@class, 'Listing__keyDetailItem__2sR9y')]/p[contains(@class, 'Text__text__x0JSc')]/descendant::text()").extract()
		for i in range(len(key_fields)):
			name = key_fields[i].replace(' ','_')
			item[name] = key_details[i]

		item['Amenities'] = response.xpath("//div[contains(@class, 'Listing__amenity__226K8')]/p[contains(@class, 'Text__text__x0JSc') and contains(@class, 'Listing__amenityLabel__CQblY')]/descendant::text()").extract()
		item['Description'] = response.xpath("//div[contains(@id, 'description')]/pre[contains(@class, 'Paragraph__text__lEhtw')]/descendant::text()").extract()
		# Url (The link to the page)
		item['Url'] = response.xpath("//meta[@property='og:url']/@content").extract()
		yield item
