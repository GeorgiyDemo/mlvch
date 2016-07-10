import requests,json,time,os,random,wget

def hosker(a):
    return ''.join([random.choice(list('123456789QWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(a)])
def rq(style,img):
	files={
		   'original_image': ('image.jpg', open(img, 'rb')),
		   'style_id': (None, style),
		   'priority': (None, '1'),
	}
	check = requests.post('http://api.mlvch.com/v1/jobs/create',files=files, headers=headers).text

	id = json.loads(check)['data']['id']

	while True:
	    jpg = json.loads(requests.get('http://api.mlvch.com/v1/jobs?id='+str(id),headers=headers).text)
	    if jpg['data']['status'] != 'completed':
	        print(jpg['data']['status'])
	        time.sleep(3)
	    else:
	        print('Completed!')
	        url  = jpg['data']['processed_img']
	        wget.download(url)
	        unique = url.split('rackcdn.com/')[1]
	        os.rename(unique,unique+'.jpg')
	        break

fakeUUID = hosker(8)+'-'+hosker(4)+'-'+hosker(4)+'-'+hosker(4)+'-'+hosker(12)
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
img = input('Type the image name\n>> ')
print('Your UUID: '+fakeUUID)
payload = 'device_id='+fakeUUID
r = requests.post('http://api.mlvch.com/v1/authorize', data=payload, headers=headers).text
token = json.loads(r)['data']['token']
headers = {'Authorization': 'token '+token}

print('Your token: '+token+'\nChoose your style img:')

style = json.loads(requests.get('http://api.mlvch.com/v1/styles/featured',headers=headers).text)
for i in range(len(style['data'])):
    print(str(style['data'][i]['id']) +' '+style['data'][i]['title']+' ('+style['data'][i]['description']+')')
choose = input('-'*40+'\nOr you can type "All"\n>> ')

if choose == 'All':
	for i in range(len(style['data'])):
		rq(str(style['data'][i]['id']),img)
else:
	rq(choose,img)