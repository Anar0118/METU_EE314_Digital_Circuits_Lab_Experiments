import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random

@cocotb.test()
async def test_register_file(dut):
    """Testbench for the Register_File module."""
    
    # Start the clock
    clock = Clock(dut.CLK, 2, units="us")  # 500 MHz clock
    cocotb.start_soon(clock.start())
    
    # Read W parameter from the DUT
    W = dut.W.value
    MAX_VALUE = (2 ** W) - 1

    # Helper functions
    async def reset_dut():
        dut.Reset.value = 1
        await RisingEdge(dut.CLK)
        dut.Reset.value = 0
        await RisingEdge(dut.CLK)
        await Timer(1, units="us")  # small delay

    async def write_register(address, data, enable=True):
        dut.Destination_Select.value = address
        dut.Data.value = data
        dut.Write_Enable.value = 1 if enable else 0
        await RisingEdge(dut.CLK)
        dut.Write_Enable.value = 0  # Disable after one clock
        await RisingEdge(dut.CLK)

    async def read_registers(src0, src1):
        dut.Source_Select_0.value = src0
        dut.Source_Select_1.value = src1
        await Timer(1, units="us")  # allow combinational logic to settle
        return int(dut.Out_0.value), int(dut.Out_1.value)
        
    for j in range(16):

        # Test sequence
        # 1. Reset the DUT
        await reset_dut()

        # After reset, all registers should be 0
        for i in range(8):
            out0, out1 = await read_registers(i, i)
            assert out0 == 0, f"Register {i} expected 0 after reset but got {out0}"
            assert out1 == 0, f"Register {i} expected 0 after reset but got {out1}"

        # 2. Write random data into each register
        test_data = {}
        for i in range(8):
            data = random.randint(0, MAX_VALUE)
            await write_register(i, data, enable=True)
            test_data[i] = data

        # 3. Read back and check
        for i in range(8):
            out0, out1 = await read_registers(i, i)
            assert out0 == test_data[i], f"Out_0 mismatch at register {i}: expected {test_data[i]}, got {out0}"
            assert out1 == test_data[i], f"Out_1 mismatch at register {i}: expected {test_data[i]}, got {out1}"
            
            
        # 4. Pick a random register to "try" writing without enabling write
        target_reg = random.randint(0, 7)
        old_value = test_data[target_reg]
        fake_data = random.randint(0, MAX_VALUE)

        await write_register(target_reg, fake_data, enable=False)  # try writing with Write_Enable = 0

        # Read back and check
        out0, out1 = await read_registers(target_reg, target_reg)
        assert out0 == old_value, (
            f"Write_Enable error at register {target_reg}: "
            f"expected {old_value}, but got {out0} after attempted disabled write"
        )
        assert out1 == old_value, (
            f"Write_Enable error at register {target_reg}: "
            f"expected {old_value}, but got {out1} after attempted disabled write"
        )

        # 5. Random read access
        for _ in range(5):
            src0 = random.randint(0, 7)
            src1 = random.randint(0, 7)
            out0, out1 = await read_registers(src0, src1)
            assert out0 == test_data[src0], f"Random read Out_0 error at register {src0}: expected {test_data[src0]}, got {out0}"
            assert out1 == test_data[src1], f"Random read Out_1 error at register {src1}: expected {test_data[src1]}, got {out1}"

    cocotb.log.info(f"All tests passed successfully with W = {W} bits!")

