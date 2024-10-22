import csv
import json

file_path = 'apartments.csv'

data = {}

with open("apartement_infos.json", "r", encoding='utf-8') as json_file:
	data = json.load(json_file)

csvData = []
maxImages = 100

for key, item in data.items():
	a = {
		'room_label': item['room_label'],
		'title': item['title']
	}
	images = []
	for i in range(maxImages):
		if (f"image_{i+1}" in item):
			images.append(item[f"image_{i+1}"])
		else:
			break
	a['images'] = json.dumps(images)
	conditions = []
	for i in range(maxImages):
		if (f"condition_list_{i+1}" in item):
			conditions.append(item[f"condition_list_{i+1}"])
		else:
			break
	a['conditions'] = json.dumps(conditions, ensure_ascii=False)
	for i in range(3):
		if (f"plan_list_item_{i+1}_value" in item):
			a[f"plan_list_item_{i+1}_label"] = item[f"plan_list_item_{i+1}_label"].replace(item[f"plan_list_item_{i+1}_value"], '')
			a[f"plan_list_item_{i+1}_value"] = item[f"plan_list_item_{i+1}_value"]
		else:
			a[f"plan_list_item_{i+1}_label"] = ''
			a[f"plan_list_item_{i+1}_value"] = ''
	for i in range(12):
		if (f"item_list_price_{i+1}" in item):
			a[f"item_list_price_{i+1}"] = item[f"item_list_price_{i+1}"]
		else:
			a[f"item_list_price_{i+1}"] = ''
	a['入居可能人数'] = item.get('outline__item_1', '')
	a['保証人'] = item.get('outline__item_2', '')
	a['ネット環境'] = item.get('outline__item_3', '')
	a['駐車場'] = item.get('outline__item_4', '')
	a['company_name'] = item.get('contract_item_1', '')
	a['契約に必要な書類'] = item.get('contract_item_1', '')
	a['その他の契約などの注意点'] = item.get('contract_item_2', '')
	a['所在地'] = item.get('location', '')
	a['アクセス'] = item.get('access', '')
	a['間取り'] = item.get('floor_plan', '')
	a['面積'] = item.get('area', '')
	a['築年数'] = item.get('year_of_construction', '')
	a['建物構造'] = item.get('building_structure', '')
	a['物件種別'] = item.get('property_type', '')
	a['建物階数'] = item.get('building_floors', '')
	a['総戸数'] = item.get('total_number_of_units', '')
	a['契約形態'] = item.get('contract_form', '')
	a['取引態様'] = item.get('transaction_mode', '')
	a['部屋の向き'] = item.get('orientation_of_the_room', '')
	a['鍵の種類'] = item.get('type_of_key', '')
	a['ベッドタイプ'] = item.get('bed_type', '')
	a['保証人'] = item.get('guarantor', '')
	a['ご利用時の注意事項'] = item.get('precautions_when_using', '')
	a['お部屋に関するご案内事項'] = item.get('information_regarding_the_room', '')
	a['入居可能日'] = item.get('available_move_in_date', '')
	csvData.append(a)

with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
	# Create a writer object
	writer = csv.DictWriter(file, fieldnames=csvData[0].keys())

	# Write the header
	writer.writeheader()

	# Write the rows
	writer.writerows(csvData)