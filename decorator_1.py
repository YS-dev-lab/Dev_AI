

## decorator : 함수를 인자로 받고 
# 새로운 기능을 추가한 새 함수를 리턴하는 구조



# 1단계 : 함수는 변수다
def say_hello():
    print("Hello!")
    

fn = say_hello
fn()


# 함수를 다른 함수의 인자로 넘길 수 있음
def run(func):
    func()
    
run(say_hello)

# ----> 데코레이터의 뿌리



# 2단계
# 함수를 리턴하는 함수

def make_greeting(name):
    def greet():
        print(f"Hi, {name}!")
    return greet 

hello = make_greeting("Alice")
hello()



# 3단계 - 데코레이터의 본체

def my_decorator(func):
    def wrapper():
        print("실행 전") # 원래 함수를 실행
        func()
        print("실행 후") # 새 함수를 리턴
        
    return wrapper

def say_hi():
    print("Hi !")

say_hi = my_decorator(say_hi) # <- decorator
say_hi()
