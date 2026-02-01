module OurCodedConverter (// This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.

    input [15:0] inencoder,     // 16-bit input for Encoder
    output [15:0] outdecoder    // 16-bit output from Decoder
);


wire [3:0] outencoder;
wire [3:0] gray;


//Fill Here
OurEncoder my_encoder(
.inencoder(inencoder),
.outencoder(outencoder)
);
 

OurBinaryToGrayConverter BtoG(
.binary(outencoder),
.gray(gray)
);


OurDecoder my_decoder(
.indecoder(gray),
.outdecoder(outdecoder)
);

endmodule