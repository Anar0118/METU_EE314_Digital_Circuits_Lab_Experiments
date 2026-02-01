module OurDecoder (
    input [3:0] indecoder,      // 4-bit input
    output reg [15:0] outdecoder // 16-bit output - Added the size of outdecoder
);

    always @(*)
	 begin // added the missing "begin" statement
        outdecoder = (16'b1 << indecoder); // Shift a single '1' to the position given by indecoder
    end

endmodule