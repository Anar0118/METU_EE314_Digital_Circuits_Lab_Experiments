module Arithmetic_Unit #(parameter W=4)
        ( // This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.
    input  [W-1:0] DATA_A,
    input  [W-1:0] DATA_B,
    input control,
    output  [W-1:0] OUT,
    output CO, OVF, N, Z
);

// Fill here
wire [W-1:0] temp;
assign temp = control ? DATA_B : ~DATA_B + 1;
assign {CO,OUT} = DATA_A + temp;
assign OVF =(DATA_A[W-1] == DATA_B[W-1] && OUT[W-1] != DATA_A[W-1] && control == 1) || 
				(DATA_A[W-1] != DATA_B[W-1] && OUT[W-1] != DATA_A[W-1] && control == 0);
				
assign N = OUT[W-1];
assign Z = (OUT == 0) ? 1 : 0;
endmodule