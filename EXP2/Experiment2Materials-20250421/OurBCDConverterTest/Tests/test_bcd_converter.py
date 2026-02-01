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

@cocotb.test()
async def test_bcd_converter(dut):
    """
    Testbench for OurBCDConverter module.
    Verifies conversion of 4-bit binary input to 8-bit BCD output.
    """
    test_failed = False  # Flag to track overall test failure

    for binary_val in range(16):  # Loop through all possible 4-bit binary values
        # Apply the binary input
        dut.inconverter.value = binary_val

        # Wait for a short delay to allow combinational logic to propagate
        await Timer(1, units='us')

        # Calculate expected BCD output
        tens = binary_val // 10  # High 4 bits (tens place)
        units = binary_val % 10  # Low 4 bits (units place)
        expected_outconverter = (tens << 4) | units

        # Check if the output matches the expected value
        if dut.outconverter.value != expected_outconverter:
            test_failed = True  # Mark overall test as failed
            cocotb.log.error(
                f"Mismatch for inconverter={binary_val}: Expected {bin(expected_outconverter)[2:].zfill(8)}, "
                f"Got {bin(dut.outconverter.value)[2:].zfill(8)}"
            )
            Log_Design(dut)
        else:
            cocotb.log.info(f"Test passed for inconverter={binary_val}. Output: {dut.outconverter.value}")

    # Final assertion for the overall result
    if test_failed:
        raise AssertionError("Some test cases failed. Check logs for details.")
    else:
        cocotb.log.info("All test cases passed successfully!")