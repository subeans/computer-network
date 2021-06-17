import sys 

def receiver(signal):
    prev = signal[0]
    if prev=='+':
        bit_stream = '1'
    else:
        bit_stream='0'
    for i in range(1,len(signal)):
        if prev != signal[i]:
            bit_stream+='1'
        else:
            bit_stream+='0'
        prev = signal[i]
    return bit_stream

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
    bit_stream = receiver(INPUT_SIGNAL)
    output_signal = bit_unstuffing(bit_stream)
    return bit_stream, output_signal 

if __name__=="__main__":
    output = main(sys.argv)
    bit_stream, output = main(sys.argv)
    print("Input bit-stream : ", sys.argv[1])
    print("after mlt3 : ",bit_stream)
    print("bit-unstuffing : ",output)