with open('slides.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        id,st,ed,is_la,url,o = line.replace('\n','').split('	')
        print(id,st,ed,is_la,url)