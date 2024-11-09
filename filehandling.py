def load_questions(subject,level):
    dif = "1"
    if level == 1:
        dif = "easy"
    elif level == 2:
        dif = "medium"
    elif level == 3:
        dif = "hard"

    question = {}
    with open(f"static/subjects/{subject}/{dif}.txt","r",encoding="utf-8") as f:
        for line in f:
            parts = line.split('|')  
            if len(parts) == 6:  
                question[parts[0]]  = [parts[1],parts[2],parts[3],parts[4],parts[5]] 
    return question
