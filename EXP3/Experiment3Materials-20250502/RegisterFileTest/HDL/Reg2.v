module Reg2 #(
    parameter W = 4
)(
    input clk,
    input reset,
    input write_enable,
    input[W-1:0] reg2_input,
    output reg [W-1:0] reg2_output
);
initial begin
	reg2_output <= {W{1'b0}};
end
always @(posedge clk) begin
    if (reset)
        reg2_output <= {W{1'b0}};
    else if (write_enable)
        reg2_output <= reg2_input;
    else
        reg2_output <= reg2_output;
end

endmodule