# v = {"r":4, "g":5, "b": 9}
# b = {"y":1, "o":2, "p": 3}
# u = dict(a)
# u["rr"] = "8"
# a["nh"] = "10"
# print(u)
# print(a)


# e2f = {"dog": "chien", "cat": "chat", "walrus": "morse"}
# e2f["english"] ="franc"

# print(len(e2f))


# a = [e2f, b, v]
# print(a[0]["cat"])

# for i in a:
#     print(i)

# print("Privet")



# city = {
#     "downtown": {"houses": 10, "shops": 5},
#     "suburb": {"houses": 20, "farms": 3}
# }

# new = {
#         "new_your": {"downtown": {"houses": 5}, "suburb": {"houses": 8}},
#         "Town": {"suburb2": {"houses": 5}, "town": {"houses": 8}},
#         "City": {"downtown": {"houses": 3}, "suburb": {"houses": 7}}
#        }


        
# for city in new:
#     for district in new[city]:
#         for state in new[city][district].values():
#         #  houses = new[city][district]["houses"]
#          print(f"В районе {district} города {city} - {state} домов")   
            





def prit_rezultat(name, family, middle):
   rezalt = f"Привет {name} {family} {middle}"
   last = f"Всего хорошего {name}"
   return rezalt, last
   

print_e = prit_rezultat("Grin", "Gtyu", "Fdsd")
print(print_e[0])

# prit_rezultat()

print_r = prit_rezultat("Potter", "Gtyu", "Fdsd")
print(print_r[1])
