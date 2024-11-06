def load_questions(subject,level):
    questions = []
    with open(f"static/subjects/{subject}/{level}.txt","r",encoding="utf-8") as f:
        for line in f:
            parts = line.split('|')  
            if len(parts) == 6:  
                question = {
                    parts[0] :[parts[1],parts[2],parts[3],parts[5],parts[5]] 
                }
                questions.append(question)
    return questions
print(load_questions("python","easy"))