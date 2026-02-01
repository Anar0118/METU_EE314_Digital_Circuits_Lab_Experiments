module Logic_Unit#(parameter W=4)
        ( // This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.
    input [W-1:0] DATA_A,
    input [W-1:0] DATA_B,
    input control,
    output [W-1:0] OUT,
    output N, Z
);
// Fill here

assign OUT = control ? DATA_A | DATA_B : DATA_A & DATA_B;
assign N = OUT[W-1];
assign Z = (OUT == 0) ? 1 : 0;
endmodule