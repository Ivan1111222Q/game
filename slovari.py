import copy


# dict_s = {1:"name", 2:"description"}
# x = dict_s[1]


# dict_w = {1:"tri", 4:"der"}
# y = dict_s | dict_w
# print(y)

# dict_t = {5:"name", 2:"description", 8:"descri"}
# sort = dict_t.get(3, "werwer")
# sotr2 = dict_t[5]
# print(sort)
# print(sotr2)


# dict_u = {"i":{"p":{"o":"were"}}, "o":"description"}
# print(dict_u["o"].title())


# gary = {"mana": 100, "inventory": ["ключ","камень","кинжал"], "здоровье": 100}
# print(f"У героя маны {gary['mana']} здоровья {gary['здоровье']} инвентарь {" :".join(gary["inventory"])}" )

# def clear_build(city,farms):
#     if farms in city:
#         del city[farms]
#     else:
#         print('Ошибка в clear_build нету здания в словаре')





# def del_build(city,houses,number):
#     if houses in city:
#         if city[houses] > number:
#             city[houses] -= number
#         else:
#             print('Домов мень чем мы можем удалить')
#     else:
#         print('Зданий нет в городе')



# def add_build(city,houses,number):
#     if houses in city:
#         city[houses] += number
#     else:
#         print('если в городе нету зданий то мы не сможем построить 10 домов')




# city = {"houses": 10, "farms": 3, "shops": 5}





# add_build(city,"houses",10)

# del_build(city,"houses",10)

# clear_build(city,"shops")



# print(city)





# def some(balboa):
#     print(balboa)


# some("eteter")


# def clear_build (city, building_type, district):
#     if building_type in city[district]:
#             del city[district][building_type]
#             print(f"Снесены все {building_type} из {district}")
#     else:
#         print(f"Ошибка: Недостаточно зданий {building_type} в районе {district}")
   



def add_building(city, building_type):
  city[building_type] = {}
  print(f"Посторили район под названием {building_type}")


  
def del_build(city, building_type, number, district):
    if building_type in city[district]:
        if city[district][building_type] >= number:
            city[district][building_type] -= number
            print(f"Удалено {number} {building_type} из {district}")
        else:
            print(f"Ошибка: Недостаточно зданий {building_type} в районе {district}")
    else:
        print(f"Ошибка: Нет зданий {building_type} в районе {district}")
    


def add_stroika(city, building_type, district, number):
         city[district][building_type] = number
         print(f"Добавлено {number} {building_type} {district}")
        
        
    

def add_build(city, building_type, number, district):
    if building_type in city[district]:
        city[district][building_type] += number
        print(f"Добавлено {number} {building_type} в {district}")
    else:
        print(f"Ошибка: Нет зданий {building_type} в районе {district}")




city = {
    "downtown": {"houses": 10, "shops": 5},
    "suburb": {"houses": 20, "farms": 3}
}




# clear_build(city, "shops","downtown")
# print(city)


# Сносим 10 домов в районе downtown
del_build(city, "houses", 10, "downtown")
print(city)

# Строим + 5 домов в районе suburb
add_build(city, "houses", 5, "suburb")
print(city)

# Строим + 10 домов в районе downtown
add_build(city, "houses", 10, "downtown")
print(city)


# Добавляем 8 заводов в районе downtown
add_stroika(city,"zavod","downtown", 8)
print(city)

# Добавляем 25 заводов в районе suburb
add_stroika(city, "zavod","suburb", 25)
print(city)

# Строим 5 ферм в районе suburb
add_build(city, "farms", 5, "suburb")
print(city)

# Постройка нового района 
add_building(city,"industrial_zone")
print(city)

# Добавляем 25 заводов в районе industrial_zone
add_stroika(city, "zavod", "industrial_zone", 25)
print(city)

# Добавляем 55 домов в районе industrial_zone
add_stroika(city, "houses", "industrial_zone", 55)
print(city)

# Добавляем 5 ферм в районе industrial_zone
add_stroika(city, "farms", "industrial_zone", 5)
print(city)



