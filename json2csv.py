import json
import re

def main():

  print("👺"*10)
  json_text='{"date":"2020-1-15",\n"data":[{"id":1,"name":"アフリカゾウ"},\n{"id":2,"name":"イノシシ"}]}'
  print("👺"*3)
  result=json2text(json_text)
  print(result)
  if "error" in result:
    print(result["error"])
  if "text" in result:
    print(result["text"])
  if "keys" in result:
    print(result["keys"])

  this_key="data"
  print("👺"*3,this_key)
  result=json2text(json_text,this_key)
  print(result)
  if "error" in result:
    print(result["error"])
  if "text" in result:
    print(result["text"])
  if "keys" in result:
    print(result["keys"])


def json2text(json_text,key=""):
  result={}
  try:
    obj=json.loads(json_text)
    result["text"]=obj2csv(obj,key)
    temp=get_keys(obj,key)
    if len(temp)>0:
      result["keys"]=get_keys(obj,key)
  except json.decoder.JSONDecodeError as e:
    error_text=str(e)
    result["error"]=get_json_error(json_text, error_text)
  return result

def get_json_error(json_text, error_text):
  # JSONのエラーメッセージをわかりやすくする。エラーとその箇所を返す。
  # Extra
  m=re.match(r"Extra.*char (\d+)",error_text)
  if(m):
    pos=int(m.groups()[0])
    part=json_text[pos-10:pos]+"👉"+json_text[pos]+"👈"+json_text[pos+1:pos+10]
    return f"余計なものがある。{part}"
  # Expecting
  m=re.match(r"Expecting.*char (\d+)",error_text)
  if(m):
    pos=int(m.groups()[0])
    part=json_text[pos-10:pos]+"👻"+json_text[pos:pos+10]
    return f"何かがない。{part}"
  else:
    return "その他。"

def get_keys(obj,key=""):
  # objが辞書型のときキーを返す
  if key in obj:
    obj=obj[key]
  if type(obj) is dict:
    keys=list(obj.keys())
    return keys
  else:
    return []


def obj2csv(obj,key=""):
  # JSONオブジェクトをテキスト（可能ならばCSVに）に変換する。
  if not key=="":
    if key in obj:
      return obj2csv(obj[key])

  if type(obj) is list:
    csv=list2csv(obj)
    return csv
  elif type(obj) is dict:
    lines=[]
    for myitem in obj.items():
      lines.append("<"+str(myitem[0])+">")
      if type(myitem[1]) is list:
        v=list2csv(myitem[1])
      else:
        v=str(myitem[1])
      lines.append(v)
    text="\n".join(lines)
    return text
  else:
    text=str(obj)
    return text

      

def list2csv(mylist,sep="\t",blank=""):
  # listをCSVに変換。
  mykeys=[]
  for part in mylist:
    mykeys+=part.keys()
  mykeys=list(set(mykeys))

  lines=[]
  lines.append(sep.join(mykeys))
  for dict in mylist:
    parts=[]
    for k in mykeys:
      if k in dict:
        parts.append(str(dict[k]))
      else:
        parts.append(blank)
    lines.append(sep.join(parts))
  csv="\n".join(lines)
  return csv


if __name__ == "__main__":
  main()