student_grades = {
    "Alice": {
        "Math": 85,
        "Science": 92,
        "History": 78
    },
    "Bob": {
        "Math": 76,
        "Science": 88,
        "History": 95
    },
    "Charlie": {
        "Math": 90,
        "Science": 80,
        "History": 82
    }
}

for name in student_grades:
    
        t = student_grades[name]["Math"]
        # o = student_grades[name]["Science"]
        # p = student_grades[name]["History"]


    
        print(f"   {name}  по математике  {t} %")
        # print(f"   {name}  по науке      {o} %")
        # print(f"   {name}  по истории     {p} %")
            
        