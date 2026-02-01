module Counter #(parameter W = 8)
(
input [1:0]  control,
input clk,
input reset,
output reg [W-1:0] counter
);


initial
begin
counter <=8'h00;
end
always@(posedge clk or posedge reset) begin
	if (reset)
		counter <= 0;
	else begin
		case(control)
		2'b00: counter <= counter;
		2'b01: counter <= counter + 1;
		2'b10: counter <= counter - 1;
		2'b11: counter <= counter;
		endcase
	end
end

endmodule