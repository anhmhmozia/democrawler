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

async def get_list_apartement_infos():
	data = {}
	apartements = {}
	count = 0
	limit = 100
	with open("apartement_infos.json", "r", encoding='utf-8') as json_file:
		data = json.load(json_file)
	with open("apartements.json", "r", encoding='utf-8') as json_file:
		apartements = json.load(json_file)
	with open("companies.json", "r", encoding='utf-8') as json_file:
		a = json.load(json_file)
	with open("prefectures.json", "r", encoding='utf-8') as json_file:
		b = json.load(json_file)
	print(len(apartements))
	print(len(a))
	print(len(b))
	for key, apartement in apartements.items():
		crawlerUrl = apartement['link']
		if ('is_crawl' in apartement):
			print(f"Crawled: {crawlerUrl}")
			continue
		count += 1
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
			if (len(info) == 0):
				continue
			info[0]['url'] = crawlerUrl
			info[0]['room_label'] = info[0]['room_label'].replace(info[0]['room_type'], '')
			info[0]['room_label'] = info[0]['room_label'].replace(info[0]['room_id'], '')
			data[apartement['id']] = info[0]
			apartements[key]['is_crawl'] = 1
			if (count > limit):
				count = 0
				print('Save data')
				with open("apartement_infos.json", "w", encoding='utf-8') as json_file:
					json.dump(data, json_file, ensure_ascii=False, indent=4)
				with open("apartements.json", "w", encoding='utf-8') as json_file:
					json.dump(apartements, json_file, ensure_ascii=False, indent=4)
	print('Save data')
	with open("apartement_infos.json", "w", encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)
	with open("apartements.json", "w", encoding='utf-8') as json_file:
		json.dump(apartements, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	asyncio.run(get_list_apartement_infos())