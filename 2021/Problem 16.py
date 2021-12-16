from operator import mul
from functools import reduce

message_raw = """0054FEC8C54DC02295D5AE9B243D2F4FEA154493A43E0E60084E61CE802419A95E38958DE4F100B9708300466AB2AB7D80291DA471EB9110010328F820084D5742D2C8E600AC8DF3DBD486C010999B44CCDBD401C9BBCE3FD3DCA624652C400007FC97B113B8C4600A6002A33907E9C83ECB4F709FD51400B3002C4009202E9D00AF260290D400D70038400E7003C400A201B01400B401609C008201115003915002D002525003A6EB49C751ED114C013865800BFCA234E677512952E20040649A26DFA1C90087D600A8803F0CA1AC1F00042A3E41F8D31EE7C8D800FD97E43CCE401A9E802D377B5B751A95BCD3E574124017CF00341353E672A32E2D2356B9EE79088032AF005E7E8F33F47F95EC29AD3018038000864658471280010C8FD1D63C080390E61D44600092645366202933C9FA2F460095006E40008742A8E70F80010F8DF0AA264B331004C52B647D004E6EEF534C8600BCC93E802D38B5311AC7E7B02D804629DD034DFBB1E2D4E2ACBDE9F9FF8ED2F10099DE828803C7C0068E7B9A7D9EE69F263B7D427541200806582E49725CFA64240050A20043E25C148CC600F45C8E717C8010E84506E1F18023600A4D934DC379B9EC96B242402504A027006E200085C6B8D51200010F89913629A805925FBD3322191A1C45A9EACB4733FBC5631A210805315A7E3BC324BCE8573ACF3222600BCD6B3997E7430F004E37CED091401293BEAC2D138402496508873967A840E00E41E99DE6B9D3CCB5E3F9A69802B2368E7558056802E200D4458AF1180010A82B1520DB80212588014C009803B2A3134DD32706009498C600664200F4558630F840188E11EE3B200C292B59124AFF9AE6775ED8BE73D4FEEFFAD4CE7E72FFBB7BB49005FB3BEBFA84140096CD5FEDF048C011B004A5B327F96CC9E653C9060174EA0CF15CA0E4D044F9E4B6258A5065400D9B68"""
#message_raw = "8A004A801A8002F478"
# message_raw = "38006F45291200"
# message_raw = "EE00D40C823060"
# message_raw = "620080001611562C8802118E34"

# message_raw = "C200B40A82"
# message_raw = "04005AC33890"
# message_raw = "9C0141080250320F1802104A08"

# Convert to binary
message_binary = ""
for c in message_raw:
    int_value = int(c, base=16)
    message_binary += str(bin(int_value))[2:].zfill(4)

print(message_binary)

total_version = 0
cursor = 0

# Read a single packet
def munch(transmission):
    global cursor, total_version
    start_cursor = cursor
    print("Preview of this packet: %s" % (transmission[start_cursor:start_cursor+20]))
    
    version = int(transmission[cursor:cursor+3], base=2)
    cursor += 3
    print ("Version is %s" % (version))
    total_version += version
    
    type_id = int(transmission[cursor:cursor+3], base=2)
    cursor += 3
    
    if type_id == 4:
        print("Found a literal")
        str_number = ""
        while transmission[cursor] == "1":
            str_number += transmission[cursor+1:cursor+1+4]
            cursor += 5
        # Get the terminating number
        str_number += transmission[cursor+1:cursor+1+4]
        cursor += 5
        return int(str_number, base=2)
        
    else:
        print("Found an operator")
        
        length_type_id = int(transmission[cursor], base=2)
        cursor += 1
        subpacket_values = []
        
        if length_type_id == 0:
            length_of_subpackets_in_bits = int(transmission[cursor:cursor+15], base=2)
            print("Looking for %s subpacket bits" % (length_of_subpackets_in_bits))
            cursor += 15
            
            endpoint = cursor + length_of_subpackets_in_bits
            
            # Accelerate packet to its end state
            #print(cursor)
            #while (cursor +1) % 4 != 0: cursor += 1
            
            while cursor < endpoint:
                subpacket_values += [munch(transmission)]
                
        elif length_type_id == 1:
            number_of_subpackets = int(transmission[cursor:cursor+11], base=2)
            print("Looking for %s subpackets" % (number_of_subpackets))
            cursor += 11
            
            # Accelerate packet to its end state
            #while cursor % 4 != 0: cursor += 1
    
            for i in range(0, number_of_subpackets):
                subpacket_values += [munch(transmission)]
                
        if type_id == 0:
            return sum(subpacket_values)
        elif type_id == 1:
            return reduce(mul, subpacket_values)
        elif type_id == 2:
            return min(subpacket_values)
        elif type_id == 3:
            return max(subpacket_values)
        elif type_id == 5:
            return 1 if subpacket_values[0] > subpacket_values[1] else 0
        elif type_id == 6:
            return 1 if subpacket_values[0] < subpacket_values[1] else 0
        elif type_id == 7:
            return 1 if subpacket_values[0] == subpacket_values[1] else 0
            
              
    # print("Complete packet: %s" % (transmission[start_cursor:cursor]))
    #return cursor

print(munch(message_binary))
print(total_version)