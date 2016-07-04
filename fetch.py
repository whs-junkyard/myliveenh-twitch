import urllib.request, json, re

raw = urllib.request.urlopen('https://api.twitch.tv/kraken/chat/emoticons') \
	.read().decode('utf-8')
emotes = json.loads(raw)

load = open('load.sh', 'w')
out = {
	'name': 'twitch',
	'emotes': {}
}

for emote in emotes['emoticons']:
	if not re.match('^[a-zA-Z0-9]+$', emote['regex']):
		continue

	image = [x for x in emote['images'] if x['emoticon_set'] == None]
	if len(image) == 0:
		continue

	image = image[0]

	load.write('wget -O {}.png {}\n'.format(
		emote['regex'],
		image['url']
	))
	out['emotes'][emote['regex']] = '{}.png'.format(emote['regex'])

print(json.dumps(out))
load.close()
