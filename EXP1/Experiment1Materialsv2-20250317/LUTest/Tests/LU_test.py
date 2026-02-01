import random
import cocotb
from cocotb.triggers import Timer
from rich.console import Console
from rich.table import Table

console = Console()

class TB:
    def __init__(self, dut):
        self.dut = dut
        # Get width from one of the LU's operand ports (assumed to be DATA_A)
        self.width = self.dut.DATA_A.value.n_bits
        self.mask = (1 << self.width) - 1
        self.min_signed = -(1 << (self.width - 1))
        self.max_signed = (1 << (self.width - 1)) - 1

        # Create a rich table for logging test results
        self.table = Table(title="Logic Unit Test Results")
        self.table.add_column("A", justify="right", style="cyan")
        self.table.add_column("B", justify="right", style="cyan")
        self.table.add_column("Op", justify="right", style="magenta")
        self.table.add_column("Expected OUT", justify="right", style="green")
        self.table.add_column("DUT OUT", justify="right", style="red")
        self.table.add_column("Expected N", justify="right", style="green")
        self.table.add_column("DUT N", justify="right", style="red")
        self.table.add_column("Expected Z", justify="right", style="green")
        self.table.add_column("DUT Z", justify="right", style="red")

    def performance_model(self, A, B, control):
        width = self.width
        mask = self.mask
        # Convert inputs to unsigned representation for bitwise operations
        A_u = A if A >= 0 else A + (1 << width)
        B_u = B if B >= 0 else B + (1 << width)

        # Determine expected result based on the selected operation:
        if control == 0:  # Bitwise AND
            op = "AND"
            res = A_u & B_u
        elif control == 1:  # Bitwise OR
            op = "OR"
            res = A_u | B_u
        else:
            op = "UNK"
            res = 0

        # Negative flag: set if the most-significant bit is 1
        expected_n = 1 if (res & (1 << (width - 1))) != 0 else 0
        # Zero flag: set if the result is zero
        expected_z = 1 if res == 0 else 0

        # Save expected values and operation string for later use
        self.expected_out = res
        self.expected_n = expected_n
        self.expected_z = expected_z
        self.operation_str = op

    async def run_random_test(self, total_test_no):
        for _ in range(total_test_no):
            # Randomly select a control value (0: AND, 1: OR)
            control = random.randint(0, 1)
            A = random.randint(self.min_signed, self.max_signed)
            B = random.randint(self.min_signed, self.max_signed)

            # Drive inputs to the DUT
            self.dut.DATA_A.value = A
            self.dut.DATA_B.value = B
            self.dut.control.value = control

            # Wait a short time (combinational LU; no clock needed)
            await Timer(1, units='us')

            # Compute expected outputs using our performance model
            self.performance_model(A, B, control)

            # Read DUT outputs (assuming ports: OUT, N, and Z)
            dut_out = self.dut.OUT.value.integer
            dut_n = self.dut.N.value.integer
            dut_z = self.dut.Z.value.integer

            # Log results in the rich table
            self.table.add_row(
                str(A), str(B), self.operation_str,
                hex(self.expected_out), hex(dut_out),
                str(self.expected_n), str(dut_n),
                str(self.expected_z), str(dut_z)
            )
            console.print(self.table)

            # Check that the DUT outputs match the expected values
            assert dut_out == self.expected_out, f"Output mismatch: expected {self.expected_out}, got {dut_out}"
            assert dut_n == self.expected_n, f"N flag mismatch: expected {self.expected_n}, got {dut_n}"
            assert dut_z == self.expected_z, f"Z flag mismatch: expected {self.expected_z}, got {dut_z}"

@cocotb.test()
async def logic_unit_test(dut):
    """
    Top-level cocotb test for the Logic Unit (LU) module.
    Assumes the LU module has the following ports:
        Inputs:  DATA_A, DATA_B (W-bit), control (1-bit)
        Outputs: OUT (W-bit), N, Z (1-bit each)
    """
    tb = TB(dut)
    await tb.run_random_test(50)
