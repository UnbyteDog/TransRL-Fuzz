import json

def taint_analysis_result(filename):
    with open(filename,'r') as f:
        result = json.load(f)
    print(result)



if __name__ == '__main__':
    filename = './SESA/json/pikachu.json'
    taint_analysis_result(filename)
    