

def cret_dict(key, valu):
  dict_s = {}
  for i in range(len(key)):
    dict_s[key[i]] = valu[i]
  print(dict_s)
  return dict_s

def change(dict_s, key, velu, operation):
  if key in dict_s.keys():
   if operation == "delete":
     rezultat = dict_s[key] - velu
     
   if operation == "add":
     rezultat = dict_s[key] + velu
     

   dict_s[key] = rezultat  
   return dict_s

key = ["home","situ","zavod"]
velu = [5,10,8]


cret_dict(key,velu)

credits = cret_dict(key,velu)



change(credits, "home", 8, "add")
print(credits)


change(credits, "situ", 1, "delete")
print(credits)


change(credits, "zavod", 15, "add")
print(credits)





