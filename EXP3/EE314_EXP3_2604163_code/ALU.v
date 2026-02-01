module ALU #(// This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.
    parameter W = 4  // Default width of 4 bits
) (
    input[1:0] Control,         // 2-bit control signal
    input[W-1:0] DATA_A,        // W-bit input DATA_A
    input[W-1:0] DATA_B,        // W-bit input DATA_B
    output reg[W-1:0] Result    // W-bit output
);

always@(*)begin
	case(Control)
	2'b00: Result = DATA_A + DATA_B;
	2'b01: Result = DATA_A + ~DATA_B + 1;
	2'b10: Result = ~DATA_B;
	2'b11: Result = {W{1'b0}};
	default: Result = {W{1'b0}};
	endcase
end


endmodule