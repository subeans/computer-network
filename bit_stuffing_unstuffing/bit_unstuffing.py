# 실행 code 형식 
# python3 bit_unstuffing_박수빈_20181614.py 000111110110011111001000

import sys 

def bit_unstuffing(unstuffing_input):
    unstuff_cnt = 0
    unstuffed=''
    for i in range(len(unstuffing_input)):
        if unstuffing_input[i]=="1" :
            unstuff_cnt+=1
            unstuffed+=unstuffing_input[i]
        else:
            if unstuff_cnt == 5:
                unstuff_cnt=0
                continue
            else:
                unstuff_cnt = 0 
                unstuffed+=unstuffing_input[i]
    return unstuffed


def main(argv):
    # INPUT_SIGNAL = str(argv[1])
    INPUT_SIGNAL = argv[1]
    bit_unstuffed = bit_unstuffing(INPUT_SIGNAL)
    return bit_unstuffed 

if __name__=="__main__":
    output = main(sys.argv)
    print(output)