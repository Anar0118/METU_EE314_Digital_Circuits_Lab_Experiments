module OurEncoder (
    input [15:0] inencoder,       // 16-bit input (one-hot encoded)
    output reg [3:0] outencoder   // 4-bit output
);

    always @(*) begin
        case (inencoder) // corrected the expression inside case()
            16'b0000_0000_0000_0001: outencoder = 4'd0;
            16'b0000_0000_0000_0010: outencoder = 4'd1;
            16'b0000_0000_0000_0100: outencoder = 4'd2;
            16'b0000_0000_0000_1000: outencoder = 4'd3;
            16'b0000_0000_0001_0000: outencoder = 4'd4;
            16'b0000_0000_0010_0000: outencoder = 4'd5;
            16'b0000_0000_0100_0000: outencoder = 4'd6;
            16'b0000_0000_1000_0000: outencoder = 4'd7;
            16'b0000_0001_0000_0000: outencoder = 4'd8;
            16'b0000_0010_0000_0000: outencoder = 4'd9;
            16'b0000_0100_0000_0000: outencoder = 4'd10;
            16'b0000_1000_0000_0000: outencoder = 4'd11;
            16'b0001_0000_0000_0000: outencoder = 4'd12;
            16'b0010_0000_0000_0000: outencoder = 4'd13;
            16'b0100_0000_0000_0000: outencoder = 4'd14;
            16'b1000_0000_0000_0000: outencoder = 4'd15;
            default: outencoder = 4'd0; // Default case if no valid input
        endcase
    end

endmodule