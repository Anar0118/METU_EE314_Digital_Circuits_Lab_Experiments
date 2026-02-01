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

def binary_to_gray(binary):
        return binary ^ (binary >> 1)

@cocotb.test()
async def test_coded_converter(dut):
 
    test_failed = False  # Flag to track overall test failure
    # Loop through all possible one-hot encoded 16-bit inputs
    for i in range(16):
        # Generate the one-hot input
        inencoder_val = 1 << i
        dut.inencoder.value = inencoder_val

        # Wait for a short delay to allow combinational logic to propagate
        await Timer(1, units='us')

        expected_outdecoder = 1 << binary_to_gray(i)

        # Check if the output matches the expected value
        if dut.outdecoder.value != expected_outdecoder:
            test_failed = True  # Mark overall test as failed
            cocotb.log.error(
                f"Mismatch for inencoder={bin(inencoder_val)[2:].zfill(16)}: Expected {bin(expected_outdecoder)[2:].zfill(16)}, "
                f"Got {dut.outdecoder.value}"
            )
            Log_Design(dut)
        else:
            cocotb.log.info(f"Test passed for inencoder={bin(inencoder_val)[2:].zfill(16)}. Output: {dut.outdecoder.value}")

    # Final assertion for the overall result
    if test_failed:
        raise AssertionError("Some test cases failed. Check logs for details.")
    else:
        cocotb.log.info("All test cases passed successfully!")