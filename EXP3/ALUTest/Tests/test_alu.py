import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random

def to_hex(obj, width=4):
    """Convert to hex with proper width handling"""
    try:
        if isinstance(obj, int):
            return f"{obj}'h{obj:0{width//4}x}"
        binary_str = bin(obj)[2:].zfill(width)
        return f"{width}'b{binary_str}"
    except:
        return str(obj)

def log_design(dut):
    """Log signal values with proper width handling"""
    width = len(dut.Result)
    print("\nCurrent ALU state:")
    print(f"Data width (W) = {width} bits")
    signals = [
        ("Control", dut.Control.value),
        ("DATA_A", dut.DATA_A.value),
        ("DATA_B", dut.DATA_B.value),
        ("Result", dut.Result.value)
    ]
    for name, value in signals:
        print(f"{name:<8}= {to_hex(value, width)}")

def alu_operation(control, a, b, width):
    """
    Testbench for ALU module.
    Gives Output depending on Control value
    """
    mask = (1 << width) - 1
    
    if control == 0b00:
        return (a + b) & mask
    elif control == 0b01:
        return (a - b) & mask
    elif control == 0b10:
        return (~b) & mask
    elif control == 0b11:
        return 0
    else:
        return 0

@cocotb.test()
async def test_alu_width_variations(dut):
    """Test ALU with different parameterized widths"""
    width = len(dut.Result)
    dut._log.info(f"\nStarting ALU tests with W = {width} bits")
    
    # Initialize
    dut.Control.value = 0
    dut.DATA_A.value = 0
    dut.DATA_B.value = 0
    await Timer(1, units='us')
    
    test_failed = False
    max_val = (1 << width) - 1
    num_random_tests = min(20, 2**width)  # Don't test too many for large widths
    
    # Test all control cases
    for control in range(4):
        dut._log.info(f"\nTesting control mode: {bin(control)}")
        
        # Edge cases
        edge_cases = [
            (0, 0),
            (0, max_val),
            (max_val, 0),
            (max_val, max_val),
            (max_val//2, max_val//2 + 1),
            ((1 << (width-1)), (1 << (width-1)))
        ]
        
        for a, b in edge_cases:
            if not await test_alu_case(dut, control, a, b, width):
                test_failed = True
        
        # Random tests
        for _ in range(num_random_tests):
            a = random.randint(0, max_val)
            b = random.randint(0, max_val)
            if not await test_alu_case(dut, control, a, b, width):
                test_failed = True
    
    
    
    if test_failed:
        raise TestFailure(f"Some ALU test cases failed for W={width}")
    else:
        dut._log.info(f"All ALU tests passed for W={width}!")

async def test_alu_case(dut, control, a, b, width):
    """Test a single ALU case with proper width handling"""
    # Set inputs
    dut.Control.value = control
    dut.DATA_A.value = a
    dut.DATA_B.value = b
    
    await Timer(1, units='us')
    
    # Get results
    expected = alu_operation(control, a, b, width)
    actual = dut.Result.value.integer
    
    # Check result
    if actual != expected:
        dut._log.error(
            f"FAIL: Control={bin(control)}, A={to_hex(a, width)}, B={to_hex(b, width)} | "
            f"Expected: {to_hex(expected, width)}, Got: {to_hex(actual, width)}"
        )
        log_design(dut)
        return False
    else:
        dut._log.info(
            f"PASS: Control={bin(control)}, A={to_hex(a, width)}, B={to_hex(b, width)} | "
            f"Result: {to_hex(actual, width)}"
        )
        return True