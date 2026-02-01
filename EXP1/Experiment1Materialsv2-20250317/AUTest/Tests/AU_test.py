import random
import cocotb
from cocotb.triggers import Timer
from rich.console import Console
from rich.table import Table

console = Console()

class TB:
    def __init__(self, dut):
        self.dut = dut
        # Get width from one of the AU's operand ports (assumed to be DATA_A)
        self.width = self.dut.DATA_A.value.n_bits
        self.mask = (1 << self.width) - 1
        self.max_value = self.mask
        self.min_signed = -(1 << (self.width - 1))
        self.max_signed = (1 << (self.width - 1)) - 1

        # Create a rich table for logging test results
        self.table = Table(title="Arithmetic Unit Test Results")
        self.table.add_column("A", justify="right", style="cyan")
        self.table.add_column("B", justify="right", style="cyan")
        self.table.add_column("Op", justify="right", style="magenta")
        self.table.add_column("Expected OUT", justify="right", style="green")
        self.table.add_column("DUT OUT", justify="right", style="red")
        self.table.add_column("Expected CO", justify="right", style="green")
        self.table.add_column("DUT CO", justify="right", style="red")
        self.table.add_column("Expected OVF", justify="right", style="green")
        self.table.add_column("DUT OVF", justify="right", style="red")
        self.table.add_column("Expected N", justify="right", style="green")
        self.table.add_column("DUT N", justify="right", style="red")
        self.table.add_column("Expected Z", justify="right", style="green")
        self.table.add_column("DUT Z", justify="right", style="red")

    def performance_model(self, A, B, control):
        width = self.width
        mask = self.mask
        # Convert inputs to unsigned representation for bitwise arithmetic
        A_u = A if A >= 0 else A + (1 << width)
        B_u = B if B >= 0 else B + (1 << width)

        # Only two operations: control 0 for subtraction, 1 for addition.
        if control == 0:  # Subtraction (A - B)
            op = "SUB"
            result = A - B
            res = result & mask
            # Carry out computed via two's complement subtraction: A + (~B + 1)
            sum_val = A_u + (((~B_u)+ 1) & mask)
            expected_co = 1 if sum_val > mask else 0
            signed_res = res - (1 << width) if res >= (1 << (width - 1)) else res
            # Overflow: occurs if A and B have different signs and result sign differs from A's sign
            expected_ovf = 1 if ((A < 0) != (B < 0)) and ((signed_res < 0) != (A < 0)) else 0
        elif control == 1:  # Addition (A + B)
            op = "ADD"
            result = A + B
            res = result & mask
            sum_val = A_u + B_u
            expected_co = 1 if sum_val > mask else 0
            signed_res = res - (1 << width) if res >= (1 << (width - 1)) else res
            # Overflow: occurs if A and B have the same sign but the result's sign differs from A's sign
            expected_ovf = 1 if ((A < 0) == (B < 0)) and ((signed_res < 0) != (A < 0)) else 0
        else:
            op = "UNK"
            res = 0
            expected_co = 0
            expected_ovf = 0

        expected_n = 1 if (res & (1 << (width - 1))) != 0 else 0
        expected_z = 1 if res == 0 else 0

        # Save expected values and operation string for later use
        self.expected_out = res
        self.expected_co = expected_co
        self.expected_ovf = expected_ovf
        self.expected_n = expected_n
        self.expected_z = expected_z
        self.operation_str = op

    async def run_random_test(self, total_test_no):
        for _ in range(total_test_no):
            # Randomly choose a control value: 0 for subtraction, 1 for addition
            control = random.randint(0, 1)
            A = random.randint(self.min_signed, self.max_signed)
            B = random.randint(self.min_signed, self.max_signed)

            # Drive inputs to the DUT
            self.dut.DATA_A.value = A
            self.dut.DATA_B.value = B
            self.dut.control.value = control

            # Wait a short time (combinational AU; no clock needed)
            await Timer(1, units='us')

            # Compute expected outputs using our performance model
            self.performance_model(A, B, control)

            # Read DUT outputs (assuming ports: OUT, CO, OVF, N, and Z)
            dut_out = self.dut.OUT.value.integer
            dut_co = self.dut.CO.value.integer
            dut_ovf = self.dut.OVF.value.integer
            dut_n = self.dut.N.value.integer
            dut_z = self.dut.Z.value.integer

            # Log results in the rich table
            self.table.add_row(
                str(A), str(B), self.operation_str,
                hex(self.expected_out), hex(dut_out),
                str(self.expected_co), str(dut_co),
                str(self.expected_ovf), str(dut_ovf),
                str(self.expected_n), str(dut_n),
                str(self.expected_z), str(dut_z)
            )
            console.print(self.table)

            # Check that the DUT outputs match the expected values
            assert dut_out == self.expected_out, f"Output mismatch: expected {self.expected_out}, got {dut_out}"
            assert dut_co == self.expected_co, f"CO mismatch: expected {self.expected_co}, got {dut_co}"
            assert dut_ovf == self.expected_ovf, f"OVF mismatch: expected {self.expected_ovf}, got {dut_ovf}"
            assert dut_n == self.expected_n, f"N flag mismatch: expected {self.expected_n}, got {dut_n}"
            assert dut_z == self.expected_z, f"Z flag mismatch: expected {self.expected_z}, got {dut_z}"

@cocotb.test()
async def arithmetic_unit_test(dut):
    """
    Top-level cocotb test for the Arithmetic Unit (AU) module.
    Assumes the AU module has the following ports:
        Inputs:  DATA_A, DATA_B (W-bit), control (1-bit)
        Outputs: OUT (W-bit), CO, OVF, N, Z (1-bit each)
    """
    tb = TB(dut)
    await tb.run_random_test(50)
