module Reg1 #(
    parameter W = 4 // default 4-bit data
)
(
    input              clk,
    input              reset,
    input  [W-1:0]      reg1_input,
    output reg [W-1:0]  reg1_output
);
initial begin
	reg1_output <= {W{1'b0}};
end
always @(posedge clk) begin
    if (reset)
        reg1_output <= {W{1'b0}};
    else
        reg1_output <= reg1_input;
end

endmodule
