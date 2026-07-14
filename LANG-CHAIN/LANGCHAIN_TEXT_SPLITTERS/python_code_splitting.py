from langchain.text_splitter import RecursiveCharacterTextSplitter,Language

text = """
class Student:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Student(name= {self.name }, age= { self.age})"
        
# example usage

student = Student("John",20)
print(student)
if __name__ == "__main__":
    student = Student("John",20)
    print(student)  

"""   

splitter = RecursiveCharacterTextSplitter.from_language(  # i can do it for many programming languages like java,php,html,etc.. , and also for markdwon cell 
    language = Language.PYTHON,  
    chunk_size = 100,
    chunk_overlap = 0,
     
)



result = splitter.split_text(text)
print(result)
print(len(result))
