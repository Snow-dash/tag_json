

#-------------------changeable var below-------------------
originPath = '' #-----where is the file,will effect the output file's location

pat=''#-----where you store the data\minecraft\tags folder in version.jar

typeli=['blocks','items','entity_types','fluids','game_events']#------what tags type you want to output

#-------------------changeable var above-------------------
import os,json,sys

sys.path.append(originPath + "\\slpp-23-master")

os.chdir(originPath)

from slpp import slpp as lua

outjs=open('out.txt','w',encoding='utf-8')

def sorteddict(dic):
    indic={}
    indic2={}
    for i in dic:
        indic[i]=dic[i]
    indic=sorted(indic)
    for i in indic:
        indic2[i]=dic[i]
    return indic2

dic={}
dic['tag_ori']={}
dic['tag']={}

jsdic={}
for root, dirs, files in os.walk(pat, topdown=False):
    loctp=''
    fix=''
    sub=root[len(pat)+1:]
    if '\\' in sub:
        loctp=sub.split('\\')[0]
        fix=sub.split('\\')[1]+'/'
    else:
        loctp=sub
        fix=''
    for fi in files:
        if loctp not in jsdic:
            jsdic[loctp]={}
        jsdic[loctp][fix+fi]=root+'\\'+fi
for tp in typeli:
    if tp not in dic['tag_ori']:
        dic['tag_ori'][str(tp)]={}
    #dic['tag_ori'][tp][js]=[]
    
    l=jsdic[tp]
    for js in l:
        if js[0:-5] not in dic['tag_ori'][tp]:
            dic['tag_ori'][tp][js[0:-5]]=[]
            temp=open(jsdic[tp][js],'r')
        tjs=json.loads(temp.read())
        for key in tjs['values']:
            if js[0:-5] not in dic['tag_ori'][tp]:
                dic['tag_ori'][tp][js[0:-5]]=[]
            dic['tag_ori'][tp][js[0:-5]].append(key)
        temp.close()
#记录原始标签 write down origin tag

tempdic={}#记录展开下级标签的标签->id对应关系 tag to ID

for tp in typeli:
    l=jsdic[tp]
    for js in l:
        temp=open(jsdic[tp][js],'r')
        tjs=json.loads(temp.read())
        if tp not in tempdic:
            tempdic[tp]={}
        tempdic[tp][js[0:-5]]=[]
        for key in tjs["values"]:#key:标签json记录的id或标签
            #print(key)
            if '#' in key:
                temp2=open(pat+'\\'+tp+'\\'+key[11:]+'.json')#二级标签
                tjs2=json.loads(temp2.read())
                for key2 in tjs2["values"]:
                    if '#' in key2:
                        temp3=open(pat+'\\'+tp+'\\'+key2[11:]+'.json')#三级标签
                        tjs3=json.loads(temp3.read())
                        for key3 in tjs3["values"]:
                            if '#' in key3:
                                #print("标签迭代次数过多\n")
                                temp4=open(pat+'\\'+tp+'\\'+key3[11:]+'.json')#四级标签
                                tjs4=json.loads(temp4.read())
                                for key4 in tjs4["values"]:
                                    if '#' in key4:
                                        print("标签迭代次数过多\n")
                                    else:
                                        tempdic[tp][js[0:-5]].append(key4[10:])
                                temp4.close()
                            else:
                                tempdic[tp][js[0:-5]].append(key3[10:])
                        temp3.close()
                    else:
                        tempdic[tp][js[0:-5]].append(key2[10:])
                temp2.close()
            else:
                tempdic[tp][js[0:-5]].append(key[10:])

for tp in typeli:
    for tag in tempdic[tp]:
        if tp not in dic['tag']:
            dic['tag'][tp]={}
        dic['tag'][tp][tag]=sorted(list(set(tempdic[tp][tag])))#去重排序 MC-223843 
        #print(dic['tag'][tp][tag])
    dic['tag'][tp]=sorteddict(dic['tag'][tp])

dic['ID']={}

for tp in typeli:
    dic['ID'][tp]={}
    for tag in tempdic[tp]:
        for objid in tempdic[tp][tag]:
            if objid not in dic['ID'][tp]:
                dic['ID'][tp][objid]=[]
            dic['ID'][tp][objid].append(tag)

for tp in typeli:
    for objid in dic['ID'][tp]:
        dic['ID'][tp][objid]=sorted(list(set(dic['ID'][tp][objid])))

outjs.write(lua.encode(dic))

outjs.close()