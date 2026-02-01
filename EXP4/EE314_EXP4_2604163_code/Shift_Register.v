module Shift_Register #(
    parameter W = 16
) (
input clk,
input reset,
input load_condition, 
input shift_condition, // 0:left, 1:right
input serial_in,
input [W-1:0] load_value,
output reg [W-1:0] register_out
);

always @(posedge clk or posedge reset) begin
	if (reset) begin
		register_out <= 0;
	end 
	else if (load_condition) begin
		register_out <= load_value;
	end 
	else begin
		if (shift_condition) begin // right shift
			register_out <= {serial_in, register_out[W-1:1]};
		end 
		else begin // left shift
			register_out <= {register_out[W-2:0], serial_in};
		end
	end
end

endmodule