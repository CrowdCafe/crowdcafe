from apiInstagram import InstagramCall


INSTAGRAM_CLIENT_ID = 'f950b57fd0b04b5f82ad0fbac1c4d5fc'
INSTAGRAM_SECRET = 'dae43415bcb4486baeb10b90c6fc9842'

apicall = InstagramCall(INSTAGRAM_CLIENT_ID,INSTAGRAM_SECRET)
dataset = apicall.getByKeyword('trento', 200)

print len(dataset)
for item in dataset:
	print item