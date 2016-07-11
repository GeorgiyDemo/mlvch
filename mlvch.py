import requests,json,time,os,random,wget,sys
link = 'http://api.mlvch.com/v1'

#UDID faker 
def hosker(a):
    return ''.join([random.choice(list('123456789QWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(a)])

#request function
def rq(style,img,i):
	files={
		   'original_image': ('image.jpg', open(img, 'rb')),
		   'style_id': (None, style),
		   'priority': (None, '1'),
	}
	check = requests.post(link+'/jobs/create',files=files, headers=headers).text
	id = json.loads(check)['data']['id']
	while True:
	    jpg = json.loads(requests.get(link+'/jobs?id='+str(id),headers=headers).text)
	    if jpg['data']['status'] != 'completed':
	        print(jpg['data']['status'])
	        time.sleep(3)
	    else:
	        print('Completed!')
	        url  = jpg['data']['processed_img']
	        wget.download(url)
	        unique = url.split('rackcdn.com/')[1]
	        os.rename(unique,str(i+1)+'.jpg')
	        break

try:
	img = sys.argv[1:][0]
except:
	print('Usage: python3 mlvch.py image.jpg')
	exit()

fakeUUID = hosker(8)+'-'+hosker(4)+'-'+hosker(4)+'-'+hosker(4)+'-'+hosker(12)
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
print('Your UUID: '+fakeUUID)
payload = 'device_id='+fakeUUID
r = requests.post(link+'/authorize', data=payload, headers=headers).text
token = json.loads(r)['data']['token']
headers = {'Authorization': 'token '+token}

print('Choose your style img:')

style = json.loads(requests.get(link+'/styles/featured',headers=headers).text)
for i in range(len(style['data'])):
    print(str(style['data'][i]['id']) +' '+style['data'][i]['title']+' ('+style['data'][i]['description']+')')
choose = input('-'*40+'\nOr you can type "all"\n>> ')

if choose == 'all':
	for i in range(len(style['data'])):
		rq(str(style['data'][i]['id']),img,i)
else:
	rq(choose,img,'ready')