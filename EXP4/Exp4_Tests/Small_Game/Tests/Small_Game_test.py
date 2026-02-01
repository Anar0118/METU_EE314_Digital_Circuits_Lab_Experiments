import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb.result import TestFailure

@cocotb.test()
async def Small_Game_test(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the module
    dut.reset.value = 1
    dut.left.value = 0
    dut.right.value = 0
    dut.attack.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay

    def flag_generator():
        if dut.attack.value == 0:
            return 0
        if dut.state.value in [1,2]:
            return 1
        return 0

    def assert_state(expected_state, message):
        if dut.CS.value != expected_state:
            raise TestFailure(f"State assertion failed: {message}. Expected {expected_state}, got {dut.CS.value}")

    def assert_outputs(move, dir_attack, attack, flag, message):
        if flag == 0:
            directional_attack_flag_temp = dut.directional_attack_flag.value
            move_flag_temp = dut.move_flag.value
        else:
            directional_attack_flag_temp = 1
            move_flag_temp = 1
        
        if (move_flag_temp != move or 
            directional_attack_flag_temp != dir_attack or 
            dut.attack_flag.value != attack):
            raise TestFailure(f"Output assertion failed: {message}. Expected (move={move}, dir_attack={dir_attack}, attack={attack}), got ({move_flag_temp}, {directional_attack_flag_temp}, {dut.attack_flag.value})")

    # Test IDLE state transitions
    dut.left.value = 1
    flag = flag_generator()
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(1, "Should transition to S_Left on left input")
    assert_outputs(1, 0, 0, flag, "In S_Left state")
    print("Passed Transition to Left")
    
    # Return to IDLE
    dut.left.value = 0
    flag = flag_generator()
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(0, "Should return to IDLE when no inputs")
    assert_outputs(0, 0, 0, flag, "Back in IDLE state")
    print("Passed Transition to IDLE")

    # Test right movement
    dut.right.value = 1
    flag = flag_generator()
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(2, "Should transition to S_Right on right input")
    assert_outputs(1, 0, 0, flag, "In S_Right state")
    print("Passed Transition to Right")
    
    # Test directional attack
    dut.attack.value = 1
    await Timer(1, units="us")  # small delay
    #print(f"Attack value: {dut.attack.value}")
    flag = flag_generator()
    #print(f"Flag Value: {flag}")
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(3, "Should transition to S_Attack_start on attack")
    assert_outputs(1, 1, 1, flag, "Attack started during movement")
    print("Passed Transition to Attack_Start")

    
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(4, "Should transition to S_Attack_active")
    assert_outputs(0, 0, 1, 0, "Attack active")
    print("Passed Transition to Attack_Active")


    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(0, "Should return to IDLE after attack")
    assert_outputs(0, 0, 0, 0, "Back in IDLE after attack sequence")
    print("Passed Transition to IDLE")


    # Test attack from IDLE
    dut.attack.value = 1
    await Timer(1, units="us")  # small delay
    flag = flag_generator()
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(3, "Should go to S_Attack_start from IDLE")
    assert_outputs(0,0,1, flag,"Error")
    print("Passed Transition to Attack_Start")

    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(4, "Should go to S_Attack_active")
    assert_outputs(0, 0, 1, 0, "Attack active")
    print("Passed Transition to Attack_Active")

    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(0, "Should return to IDLE")
    assert_outputs(0, 0, 0, 0, "Back in IDLE after attack sequence")
    print("Passed Transition to IDLE")
    
    

    # Reset test
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay
    assert_state(0, "Reset should return to IDLE")
    assert_outputs(0, 0, 0, 0, "Outputs should be zero after reset")
    dut.reset.value = 0
    print("Reseted")
    
    # Test movement after attack
    dut.left.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # small delay

    dut.attack.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # at Attack_Start

    await RisingEdge(dut.clk)
    await Timer(1, units="us")  # at Attack_Active

    await RisingEdge(dut.clk)  # Complete attack sequence
    await Timer(1, units="us")  # at IDLE
    print("Passed Complete Attack Sequence")

    # Print success message if all tests pass
    dut._log.info("All tests passed successfully!")