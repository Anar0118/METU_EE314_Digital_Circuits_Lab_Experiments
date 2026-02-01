module Decoder(
	input[2:0] dec_input,
	output reg [7:0] dec_output
);

always @(*)begin	 
	dec_output = (8'b1 << dec_input);
	end


endmodule