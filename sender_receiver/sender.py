import sys 

def mlt(input_signal):
    output_signal = ''
    last_zero =''
    prev = input_signal[0]
    if prev == '0':
        output_signal +='0'
        prev = '0'
    else : 
        output_signal +='+'
        prev='+'
    for i in range(1,len(input_signal)):
        if input_signal[i]=='0':
    #         print('not_changed')
            output_signal +=prev 
        elif input_signal[i] =='1' and prev!='0':
    #         print('changed to zero')
            output_signal +='0'
            last_zero = prev
            prev = '0'
        elif input_signal[i]=='1' and prev =='0' :
    #         print('changed to pos or neg')
            if last_zero == '':
                output_signal +='+'
                prev='+'
            elif last_zero == '+':
                output_signal += '-'
                prev='-'
            elif last_zero=='-':
                output_signal+='+'
                prev='+'
    return output_signal

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
    stuffed_signal = bit_stuffing(INPUT_SIGNAL)
    output_signal = mlt(stuffed_signal)
    return stuffed_signal, output_signal 

if __name__=="__main__":
    stuffed, output = main(sys.argv)
    print("FRAME : ", sys.argv[1])
    print("bit-stuffing : ",stuffed)
    print("after mlt3 : ",output)