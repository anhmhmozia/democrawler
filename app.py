from flask import Flask, render_template, request, redirect, url_for, jsonify
import asyncio
import json
from urllib.parse import urlparse, parse_qs
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
async def submit_form():
    data = request.json
    crawlerData = []
    crawlerUrl = data['url']
    base_selector = data['base_selector']
    fields = data['fields']
    schema = {
        "name": "Demo crawler",
        "baseSelector": base_selector,
        "fields": []
    }
    for field in fields:
        if (field['type'] == 'text'):
            schema['fields'].append(field)
        elif (field['type'] == 'image'):
            schema['fields'].append({
                'name': field['name'],
                'selector': field['selector'],
                'type': 'attribute',
                'attribute': 'src',
            })
        else:
            schema['fields'].append({
                'name': field['name'],
                'selector': field['selector'],
                'type': 'attribute',
                'attribute': 'href',
            })
        extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=crawlerUrl,
                extraction_strategy=extraction_strategy,
                bypass_cache=True
            )

            assert result.success, "Failed to crawl the page"
            crawlerData = json.loads(result.extracted_content)
    return jsonify({"message": crawlerData}), 200
    
if __name__ == '__main__':
    app.run(debug=True)
