module OurBCDConverter (
    input [3:0] inconverter,      // 4-bit binary input
    output reg [7:0] outconverter // 8-bit BCD output (High 4 bits for tens, Low 4 bits for units)
);

    reg [3:0] tens;
    reg [3:0] units;

    always @(*) begin
        // Use if-else logic for conversion
        if (inconverter >= 4'b1010) begin
            tens = 4'b0001;          // Add 1 to tens for values >= 10
            units = inconverter - 4'b1010;
        end else begin
            tens = 4'b0000;          // No tens for values < 10
            units = inconverter;     // Units remain the same
        end

        // Combine tens and units into BCD output
        outconverter = {tens, units};
    end

endmodule