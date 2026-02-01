module MUXx#(parameter W=4 // default 4-bit data
)
(
	input  [2:0]   select,
	input  [W-1:0] mux_input_0,
	input  [W-1:0] mux_input_1,
	input  [W-1:0] mux_input_2,
   input  [W-1:0] mux_input_3,
   input  [W-1:0] mux_input_4,
   input  [W-1:0] mux_input_5,
   input  [W-1:0] mux_input_6,
   input  [W-1:0] mux_input_7,
	output reg [W-1:0] mux_output
);

always@(*) begin
	case(select)
	3'b000: mux_output = mux_input_0;
	3'b001: mux_output = mux_input_1;
	3'b010: mux_output = mux_input_2;
	3'b011: mux_output = mux_input_3;
	3'b100: mux_output = mux_input_4;
	3'b101: mux_output = mux_input_5;
	3'b110: mux_output = mux_input_6;
	3'b111: mux_output = mux_input_7;
	default: mux_output = {W{1'b0}};
	endcase
end

endmodule