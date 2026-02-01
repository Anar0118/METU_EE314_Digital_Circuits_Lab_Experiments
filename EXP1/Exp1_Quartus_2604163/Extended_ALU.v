module Extended_ALU #(parameter W = 4)(
	input [W-1:0]   DATA_A,
	input [W-1:0]   DATA_B,
	input [1:0]   control,
	output [W-1:0] OUT,
	output  CO, OVF, N, Z
);

wire [W-1:0] ext_out;

ALU #(W) my_ALU (
	.DATA_A(DATA_A),
	.DATA_B(DATA_B),
	.control(control),
	.OUT(ext_out),
	.CO(CO),
	.OVF(OVF),
	.N(N),
	.Z(Z)
);

assign OUT = ext_out<<1;

endmodule