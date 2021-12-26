import requests
import lxml.html
import json

html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)

new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

game_tags = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = [tag.text_content() for tag in game_tags]
tags = [tag.split(', ') for tag in tags]

platform_divs = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []

for game in platform_divs:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)

output = []
for info in zip(titles,prices,tags,total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['price'] = info[1]
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)

jsonString = json.dumps(output)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
