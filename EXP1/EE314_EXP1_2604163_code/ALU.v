module ALU #(
    parameter W = 4
)(// This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.
    input [W-1:0]   DATA_A,
    input [W-1:0]   DATA_B,
    input [1:0]   control,
    output [W-1:0] OUT,
    output  CO, OVF, N, Z
);

// Fill here
wire [W-1:0] au_out, lu_out;
wire au_co, au_ovf;


Arithmetic_Unit #(W) AU (
    .DATA_A(DATA_A),
    .DATA_B(DATA_B),
    .control(control[0]),
    .OUT(au_out),
    .CO(au_co),
    .OVF(au_ovf)
);

Logic_Unit #(W) LU (
    .DATA_A(DATA_A),
    .DATA_B(DATA_B),
    .control(control[0]),
    .OUT(lu_out)
);

assign OUT = control[1] ? au_out : lu_out;
assign CO  = control[1] ? au_co : 1'b0;
assign OVF = control[1] ? au_ovf : 1'b0;
assign N   = OUT[W-1];
assign Z   = (OUT == 0) ? 1'b1 : 1'b0;

endmodule