import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def counter_test(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    dut.reset.value = 1
    dut.control.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    
    # Test increment
    dut.control.value = 1  # 01 for increment
    for i in range(5):
        await RisingEdge(dut.clk)
        await Timer(1, units="us")  # small delay
        assert dut.counter.value == i+1, f"Counter failed at increment {i}: counter -- {dut.counter.value}  expected -- {i+1}"
        print(f"Passed the increment: counter -- {dut.counter.value}")
    
    # Test decrement
    dut.control.value = 2  # 10 for decrement
    for i in range(4, -1, -1):
        await RisingEdge(dut.clk)
        await Timer(1, units="us")  # small delay
        assert dut.counter.value == i, f"Counter failed at decrement {i}: counter -- {dut.counter.value}  expected -- {i}"
        print(f"Passed the decrement: counter -- {dut.counter.value}")
    
    # Test hold
    dut.control.value = 0
    current = dut.counter.value
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert dut.counter.value == current, "Counter failed at hold"
    print("Passed the hold")