# https://github.com/unclecode/crawl4ai
import re
import asyncio
import json
import random
from urllib.parse import urlparse, parse_qs
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

def get_proxy():
	proxies = [
		'38.153.66.221:8800',
		'45.66.238.179:8800',
		'80.65.222.227:8800',
		'5.253.118.134:8800',
		'5.253.118.217:8800',
		'38.153.66.104:8800',
		'5.253.118.187:8800',
		'45.66.238.69:8800',
		'5.253.118.174:8800',
		'80.65.222.51:8800',
	]
	proxy = random.choice(proxies)
	return f"http://{proxy}"

async def get_list_pref():
	crawlerUrl = 'https://weeklyandmonthly.com/srchcompany/'
	schema = {
		"name": "Get list pref",
		"baseSelector": ".srchcompany__map ul li .box .on",
		"fields": [
			{
				"name": "name",
				"type": "text",
			},
			{
				"name": "link",
				"type": "attribute",
				"attribute": "href",
			}
		]
	}
	extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

	async with AsyncWebCrawler(verbose=True) as crawler:
		result = await crawler.arun(
			url=crawlerUrl,
			extraction_strategy=extraction_strategy,
			bypass_cache=True
		)

		assert result.success, "Failed to crawl the page"
		data = json.loads(result.extracted_content)
		print(f"Successfully extracted {len(data)} news teasers")
		with open("prefectures.json", "w", encoding='utf-8') as json_file:
			json.dump(data, json_file, ensure_ascii=False, indent=4)

async def get_list_companies():
	data = []
	prefs = []
	with open('companies.json', 'r') as json_file:
		data = json.load(json_file)
	with open("prefectures.json", "r", encoding='utf-8') as json_file:
		prefs = json.load(json_file)
	for pref in prefs:
		crawlerUrl = pref['link']
		maxPage = 10000
		match = re.search(r'pref_(\d+)', crawlerUrl)
		prefId = 0
		if match:
			prefId = match.group(1)
		for page in range(maxPage):
			schema = {
				"name": "Get list company of pref",
				"baseSelector": ".srchcomp__list .srchcomp__item h3.srchcomp__name",
				"fields": [
					{
						"name": "name",
						"selector": "a",
						"type": "text",
					},
					{
						"name": "link",
						"selector": "a[href]",
						"type": "attribute",
						"attribute": "href",
					}
				]
			}
			extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

			proxy = get_proxy()

			async with AsyncWebCrawler(verbose=True) as crawler:
				result = await crawler.arun(
					url=crawlerUrl+'?page='+str(page + 1),
					extraction_strategy=extraction_strategy,
					bypass_cache=True,
					proxy=proxy
				)

				assert result.success, "Failed to crawl the page"
				companies = json.loads(result.extracted_content)
				print(f"Get companies pref {prefId} page {page + 1}: {len(companies)} companies")
				if (len(companies) == 0):
					break
				else:
					for company in companies:
						companyId = 0
						companyIdRex = re.search(r'dtl_(\d+)', company['link'])
						if companyIdRex:
							companyId = companyIdRex.group(1)
						data[str(f"{prefId}_{companyId}")] = {
							'name': company['name'],
							'link': company['link'],
							'pref_id': prefId,
							'company_id': companyId
						}
			
	with open("companies.json", "w", encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

async def get_list_apartements():
	data = {}
	companies = {}
	pre_company_id = ''
	with open("apartements.json", "r", encoding='utf-8') as json_file:
		data = json.load(json_file)
	with open("companies.json", "r", encoding='utf-8') as json_file:
		companies = json.load(json_file)
	for key, company in companies.items():
		crawlerUrl = f"https://weeklyandmonthly.com/srch/company/{company['pref_id']}/{company['company_id']}/"
		if ('is_crawl' in company and company['is_crawl'] == 1):
			print(f"Crawled: {crawlerUrl}")
			continue
		maxPage = 10000
		for page in range(maxPage):
			schema = {
				"name": "Get list departments of company",
				"baseSelector": ".roomitemlist__item .item__bottom .item__btn",
				"fields": [
					{
						"name": "link",
						"selector": "a[href]",
						"type": "attribute",
						"attribute": "href",
					}
				]
			}
			extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

			proxy = get_proxy()

			async with AsyncWebCrawler(verbose=True) as crawler:
				result = await crawler.arun(
					url=crawlerUrl+'?page='+str(page + 1),
					extraction_strategy=extraction_strategy,
					bypass_cache=True,
					proxy=proxy
				)

				assert result.success, "Failed to crawl the page"
				apartements = json.loads(result.extracted_content)
				print(f"Get apartements page {page + 1}: {len(apartements)} apartements")
				if (len(apartements) == 0):
					if (page == 0):
						if (pre_company_id != ''):
							companies[pre_company_id]['is_crawl'] = 0
						with open("apartements.json", "w", encoding='utf-8') as json_file:
							json.dump(data, json_file, ensure_ascii=False, indent=4)
						with open("companies.json", "w", encoding='utf-8') as json_file:
							json.dump(companies, json_file, ensure_ascii=False, indent=4)
						return False
					break
				else:
					companies[key]['is_crawl'] = 1
					for apartement in apartements:
						parsed_url = urlparse(apartement['link'])
						query_params = parse_qs(parsed_url.query)
						apartement_id = str(query_params.get('id', 0)[0])
						data[apartement_id] = {
							'link': apartement['link'],
							'id': apartement_id,
						}
		pre_company_id = key
			
	with open("apartements.json", "w", encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

async def get_list_apartement_infos():
	data = []
	apartements = []
	with open("apartements.json", "r", encoding='utf-8') as json_file:
		apartements = json.load(json_file)
	with open("companies.json", "r", encoding='utf-8') as json_file:
		a = json.load(json_file)
	with open("prefectures.json", "r", encoding='utf-8') as json_file:
		b = json.load(json_file)
	print(len(apartements))
	print(len(a))
	print(len(b))
	return False
	for apartement in apartements:
		crawlerUrl = apartement['link']
		schema = {
			"name": "Get company detail",
			"baseSelector": ".content .inner",
			"fields": [
				{
					"name": "room_label",
					"selector": "h1.title__main",
					"type": "text",
				},
				{
					"name": "room_type",
					"selector": "h1.title__main .title__main-label",
					"type": "text",
				},
				{
					"name": "room_id",
					"selector": "h1.title__main .title__main-room-id",
					"type": "text",
				},
				{
					"name": "title",
					"selector": "p.title__catch",
					"type": "text",
				},
				{
					"name": "image_1",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.main > img",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "image_2",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.sub > img",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "image_3",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.sub > div > img:nth-child(1)",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "image_4",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.sub > div > img:nth-child(2)",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "image_5",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.sub > div > img:nth-child(3)",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "image_6",
					"selector": "div.photo.t-bdc--primary > div.photo__col2.sub > div > img:nth-child(4)",
					"type": "attribute",
					"attribute": "src",
				},
				{
					"name": "plan_list_item_1_label",
					"selector": "ul.plan-list > li:nth-child(1) > h3",
					"type": "text",
				},
				{
					"name": "plan_list_item_1_value",
					"selector": "ul.plan-list > li:nth-child(1) > h3 span",
					"type": "text",
				},
				{
					"name": "plan_list_item_2_label",
					"selector": "ul.plan-list > li:nth-child(2) > h3",
					"type": "text",
				},
				{
					"name": "plan_list_item_2_value",
					"selector": "ul.plan-list > li:nth-child(2) > h3 > span",
					"type": "text",
				},
				{
					"name": "plan_list_item_3_label",
					"selector": "ul.plan-list > li:nth-child(3) > h3",
					"type": "text",
				},
				{
					"name": "plan_list_item_3_value",
					"selector": "ul.plan-list > li:nth-child(3) > h3 span",
					"type": "text",
				},
				{
					"name": "outline__item_1",
					"selector": "div.detail__side > ul > li:nth-child(1) > span.outline__data",
					"type": "text",
				},
				{
					"name": "outline__item_2",
					"selector": "div.detail__side > ul > li:nth-child(2) > span.outline__data",
					"type": "text",
				},
				{
					"name": "outline__item_3",
					"selector": "div.detail__side > ul > li:nth-child(3) > span.outline__data",
					"type": "text",
				},
				{
					"name": "outline__item_4",
					"selector": "div.detail__side > ul > li:nth-child(4) > span.outline__data",
					"type": "text",
				},
				{
					"name": "item_list_price_1",
					"selector": "ul.plan-list > li:nth-child(1) > div > ul > li:nth-child(1) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_2",
					"selector": "ul.plan-list > li:nth-child(1) > div > ul > li:nth-child(2) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_3",
					"selector": "ul.plan-list > li:nth-child(1) > div > ul > li:nth-child(3) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_4",
					"selector": "ul.plan-list > li:nth-child(1) > div > ul > li:nth-child(4) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_5",
					"selector": "ul.plan-list > li:nth-child(2) > div > ul > li:nth-child(1) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_6",
					"selector": "ul.plan-list > li:nth-child(2) > div > ul > li:nth-child(2) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_7",
					"selector": "ul.plan-list > li:nth-child(2) > div > ul > li:nth-child(3) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_8",
					"selector": "ul.plan-list > li:nth-child(2) > div > ul > li:nth-child(4) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_9",
					"selector": "ul.plan-list > li:nth-child(3) > div > ul > li:nth-child(1) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_10",
					"selector": "ul.plan-list > li:nth-child(3) > div > ul > li:nth-child(2) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_11",
					"selector": "ul.plan-list > li:nth-child(3) > div > ul > li:nth-child(3) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "item_list_price_12",
					"selector": "ul.plan-list > li:nth-child(3) > div > ul > li:nth-child(4) > p:nth-child(2)",
					"type": "text",
				},
				{
					"name": "contract_item_1",
					"selector": "div.contract > div:nth-child(2) > p",
					"type": "text",
				},
				{
					"name": "contract_item_2",
					"selector": "div.contract > div:nth-child(3) > p",
					"type": "text",
				},
				{
					"name": "location",
					"selector": "div.room__outline > table > tbody > tr:nth-child(1) > td",
					"type": "text",
				},
				{
					"name": "access",
					"selector": "div.room__outline > table > tbody > tr:nth-child(2) > td",
					"type": "text",
				},
				{
					"name": "floor_plan",
					"selector": "div.room__outline > table > tbody > tr:nth-child(3) > td:nth-child(2)",
					"type": "text",
				},
				{
					"name": "area",
					"selector": "div.room__outline > table > tbody > tr:nth-child(3) > td:nth-child(4)",
					"type": "text",
				},
				{
					"name": "year_of_construction",
					"selector": "div.room__outline > table > tbody > tr:nth-child(4) > td",
					"type": "text",
				},
				{
					"name": "building_structure",
					"selector": "div.room__outline > table > tbody > tr:nth-child(5) > td",
					"type": "text",
				},
				{
					"name": "property_type",
					"selector": "div.room__outline > table > tbody > tr:nth-child(6) > td",
					"type": "text",
				},
				{
					"name": "building_floors",
					"selector": "div.room__outline > table > tbody > tr:nth-child(7) > td:nth-child(2)",
					"type": "text",
				},
				{
					"name": "total_number_of_units",
					"selector": "div.room__outline > table > tbody > tr:nth-child(7) > td:nth-child(4)",
					"type": "text",
				},
				{
					"name": "contract_form",
					"selector": "div.room__outline > table > tbody > tr:nth-child(8) > td:nth-child(2)",
					"type": "text",
				},
				{
					"name": "transaction_mode",
					"selector": "div.room__outline > table > tbody > tr:nth-child(8) > td:nth-child(4)",
					"type": "text",
				},
				{
					"name": "orientation_of_the_room",
					"selector": "div.room__outline > table > tbody > tr:nth-child(9) > td:nth-child(2)",
					"type": "text",
				},
				{
					"name": "type_of_key",
					"selector": "div.room__outline > table > tbody > tr:nth-child(9) > td:nth-child(4)",
					"type": "text",
				},
				{
					"name": "bed_type",
					"selector": "div.room__outline > table > tbody > tr:nth-child(10) > td",
					"type": "text",
				},
				{
					"name": "guarantor",
					"selector": "div.room__outline > table > tbody > tr:nth-child(11) > td",
					"type": "text",
				},
				{
					"name": "precautions_when_using",
					"selector": "div.room__outline > table > tbody > tr:nth-child(12) > td",
					"type": "text",
				},
				{
					"name": "information_regarding_the_room",
					"selector": "div.room__outline > table > tbody > tr:nth-child(13) > td",
					"type": "text",
				},
				{
					"name": "available_move_in_date",
					"selector": "div.room__outline > table > tbody > tr:nth-child(14) > td",
					"type": "text",
				}
			]
		}
		for i in range(50):
			schema['fields'].append({
				"name": f"condition_list_{i}",
				"selector": f"ul.conditionlist  li:nth-child({i})",
				"type": "text",
			})
		# for i in range(100):
		# 	schema['fields'].append({
		# 		"name": f"image_{i}",
		# 		"selector": f"#modaal > div.modaal__gallery.slick-initialized.slick-slider > div.slick-list.draggable > div > div:nth-child({i}) > div > div",
		# 		"type": "text",
		# 	})
		extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
		async with AsyncWebCrawler(verbose=True) as crawler:
			result = await crawler.arun(
				url=crawlerUrl,
				extraction_strategy=extraction_strategy,
				bypass_cache=True
			)

			assert result.success, "Failed to crawl the page"
			info = json.loads(result.extracted_content)
			info[0]['url'] = crawlerUrl
			info[0]['room_label'] = info[0]['room_label'].replace(info[0]['room_type'], '')
			info[0]['room_label'] = info[0]['room_label'].replace(info[0]['room_id'], '')
			data.append(info)
			
	with open("apartement_infos.json", "w", encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	# asyncio.run(get_list_pref())
	# asyncio.run(get_list_companies())
	asyncio.run(get_list_apartements())
	# asyncio.run(get_list_apartement_infos())