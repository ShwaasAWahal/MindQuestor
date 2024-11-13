import random
random_set = set()
random_set_1 =set()

def load_questions(subject,level):
    global random_set
    if level != 4:
        dif = None
        if level == 1:
            dif = "easy"
        elif level == 2:
            dif = "medium"
        elif level == 3:
            dif = "hard"

    
        while len(random_set) < 5:
            random_set.add(random.randint(0 , 9))
        
        print(random_set)
        question = {}
        with open(f"static/subjects/{subject}/{dif}.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
            for i in random_set:
                line = lines[i]
                parts = line.split('|')
                if len(parts) == 6:  
                    question[parts[0]]  = [parts[1],parts[2],parts[3],parts[4],parts[5]]
            
                
        return question
    else:
        while len(random_set_1) < 4:
            random_set_1.add(random.randint(0 , 9))
        print(random_set_1)
        question = {}

        feasy = open(f"static/subjects/{subject}/easy.txt" , "r" ,encoding="utf-8")
        lines_easy = feasy.readlines()
        for i in random_set_1:
            line_easy = lines_easy[i]
            parts_easy = line_easy.split("|")
            if len(parts_easy) == 6:
                question[parts_easy[0]] = [parts_easy[1] , parts_easy[2] , parts_easy[3] , parts_easy[4] , parts_easy[5] , 10]

        fmed = open(f"static/subjects/{subject}/medium.txt" , "r" ,encoding="utf-8")
        lines_med = fmed.readlines()
        for i in random_set_1:
            line_med = lines_med[i]
            parts_med = line_med.split("|")
            
            question[parts_med[0]] = [parts_med[1] , parts_med[2] , parts_med[3] , parts_med[4] , parts_med[5] , 20]

        fhard = open(f"static/subjects/{subject}/hard.txt" , "r" ,encoding="utf-8")
        lines_hard = fhard.readlines()
        for i in random_set_1:
            line_hard = lines_hard[i]
            parts_hard = line_hard.split("|")
            
            question[parts_hard[0]] = [parts_hard[1] , parts_hard[2] , parts_hard[3] , parts_hard[4] , parts_hard[5] , 30]
        feasy.close()
        fmed.close()
        fhard.close()
        print(len(question))
        return question
    
        
        