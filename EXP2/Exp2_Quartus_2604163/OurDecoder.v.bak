module OurDecoder (
    input [3:0] indecoder,      // 4-bit input
    output reg outdecoder // 16-bit output
);

    always @(*)
        outdecoder = (16'b1 << indecoder); // Shift a single '1' to the position given by indecoder
    end

endmodule