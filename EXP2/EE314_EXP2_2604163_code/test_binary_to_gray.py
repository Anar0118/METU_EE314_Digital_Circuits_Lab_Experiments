import cocotb
from cocotb.triggers import Timer

def to_hex(obj): # Convert to hex only if signal is longer than 16 bits
    try:
        binary_str = str(obj)
        binary_str = binary_str.strip()
        if(len(binary_str)>=16  and  binary_str.replace("1","").replace("0","") == ""):
            value = int(binary_str,2)
            hex_len = (len(binary_str)+3)//4
            hex_str = format(value, '0{}x'.format(hex_len))
            return "0x"+hex_str
    except Exception as e:
        pass
    return obj
#This function helps us see the values of the signals in our design.
def Log_Design(dut):
    #Log whatever signal you want from the datapath, called before positive clock edge
    s1 = "dut"
    obj1 = dut
    wires = []
    submodules = []
    for attribute_name in dir(obj1):
        attribute = getattr(obj1, attribute_name)
        if attribute.__class__.__module__.startswith('cocotb.handle'):
            if(attribute.__class__.__name__ == 'ModifiableObject'):
                wires.append((attribute_name, to_hex(attribute.value)) )
            elif(attribute.__class__.__name__ == 'HierarchyObject'):
                submodules.append((attribute_name, attribute.get_definition_name()) )
            elif(attribute.__class__.__name__ == 'HierarchyArrayObject'):
                submodules.append((attribute_name, f"[{len(attribute)}]") )
            elif(attribute.__class__.__name__ == 'NonHierarchyIndexableObject'):
                wires.append((attribute_name, [to_hex(v) for v in attribute.value] ) )
            #else:
                #print(f"{attribute_name}: {type(attribute)}")
                
        #else:
            #print(f"{attribute_name}: {type(attribute)}")
    #for sub in submodules:
    #    print(f"{s1}.{sub[0]:<16}is {sub[1]}")
    for wire in wires:
        print(f"{s1}.{wire[0]:<16}= {wire[1]}")

def binary_to_gray(binary_val):
    binary_to_gray_dict = {
    # Binary (4-bit) : Gray Code (4-bit)
    '0000': '0000',  # 0 → 0
    '0001': '0001',  # 1 → 1
    '0010': '0011',  # 2 → 3
    '0011': '0010',  # 3 → 2
    '0100': '0110',  # 4 → 6
    '0101': '0111',  # 5 → 7
    '0110': '0101',  # 6 → 5
    '0111': '0100',  # 7 → 4
    '1000': '1100',  # 8 → 12
    '1001': '1101',  # 9 → 13
    '1010': '1111',  # 10 → 15
    '1011': '1110',  # 11 → 14
    '1100': '1010',  # 12 → 10
    '1101': '1011',  # 13 → 11
    '1110': '1001',  # 14 → 9
    '1111': '1000'   # 15 → 8
    }
    binary_str = format(binary_val, '04b')
    gray_str = binary_to_gray_dict[binary_str]
    return int(gray_str, 2)

@cocotb.test()
async def test_binary_to_gray(dut):
    """
    Testbench for OurBinaryToGrayConverter module.
    Verifies conversion of 4-bit binary input to 8-bit gray code output.
    """
    test_failed = False  # Flag to track overall test failure

    for binary_val in range(16):  # Loop through all possible 4-bit binary values
        # Apply the binary input
        dut.binary.value = binary_val

        # Wait for a short delay to allow combinational logic to propagate
        await Timer(1, units='us')

        # Calculate expected Gray Code output
        expected_gray = binary_to_gray(binary_val)

        # Check if the output matches the expected value
        if dut.gray.value != expected_gray:
            test_failed = True  # Mark overall test as failed
            cocotb.log.error(
                f"Mismatch for binary={binary_val}: Expected {bin(expected_gray)[2:].zfill(4)}, "
                f"Got {bin(dut.gray.value)[2:].zfill(4)}"
            )
            Log_Design(dut)
        else:
            cocotb.log.info(f"Test passed for binary={binary_val}. Output: {dut.gray.value}")

    # Final assertion for the overall result
    if test_failed:
        raise AssertionError("Some test cases failed. Check logs for details.")
    else:
        cocotb.log.info("All test cases passed successfully!")