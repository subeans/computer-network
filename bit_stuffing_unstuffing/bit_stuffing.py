# 실행 code 형식 
# python3 bit_stuffing_박수빈_20181614.py 0001111111001111101000



import sys 

def bit_stuffing(input_data):
    stuff_cnt = 0
    stuffed=''
    for i in range(len(input_data)):
        if input_data[i]=="1" :
            stuff_cnt+=1
            if stuff_cnt == 5 :
                stuffed+=input_data[i] 
                stuffed += '0'
                stuff_cnt = 0
            elif stuff_cnt!=5:
                stuffed+=input_data[i]
        else:
            stuff_cnt = 0 
            stuffed+=input_data[i]
    return stuffed


def main(argv):
    # INPUT_SIGNAL = str(argv[1])
    INPUT_SIGNAL = argv[1]
    bit_stuffed = bit_stuffing(INPUT_SIGNAL)
    return bit_stuffed 

if __name__=="__main__":
    output = main(sys.argv)
    print(output)