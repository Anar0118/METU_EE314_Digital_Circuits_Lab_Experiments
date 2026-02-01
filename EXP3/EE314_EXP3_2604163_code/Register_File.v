module Register_File #(
    parameter W = 4                 // Data width parameter (default 4 bits)
)(
    input CLK,                 // Clock signal
    input Reset,               // Reset signal (active high)
    input [W-1:0] Data,        // W-bit data input
    input [2:0] Destination_Select,  // 3-bit write address
    input Write_Enable,        // Write enable signal
    input [2:0] Source_Select_0,  // 3-bit read address for port 0
    input [2:0] Source_Select_1,  // 3-bit read address for port 1
    output [W-1:0] Out_0,       // W-bit output for port 0
    output [W-1:0] Out_1        // W-bit output for port 1
);

wire [7:0] write_enables;
wire [W-1:0] reg_outputs [0:7];

Decoder write_decoder(
.dec_input(Destination_Select),
.dec_output(write_enables)
 );

 
genvar i;
generate
for (i = 0; i < 8; i = i + 1) begin: connections
	Reg2 #(.W(W)) register(
	.clk(CLK),
	.reset(Reset),
	.write_enable(Write_Enable & write_enables[i]),
	.reg2_input(Data),
	.reg2_output(reg_outputs[i])
			);
	  end
 endgenerate
 
 
MUXx #(.W(W)) output_mux_0(
.select(Source_Select_0),
.mux_input_0(reg_outputs[0]),
.mux_input_1(reg_outputs[1]),
.mux_input_2(reg_outputs[2]),
.mux_input_3(reg_outputs[3]),
.mux_input_4(reg_outputs[4]),
.mux_input_5(reg_outputs[5]),
.mux_input_6(reg_outputs[6]),
.mux_input_7(reg_outputs[7]),
.mux_output(Out_0)
);
 
 
MUXx #(.W(W)) output_mux_1(
.select(Source_Select_1),
.mux_input_0(reg_outputs[0]),
.mux_input_1(reg_outputs[1]),
.mux_input_2(reg_outputs[2]),
.mux_input_3(reg_outputs[3]),
.mux_input_4(reg_outputs[4]),
.mux_input_5(reg_outputs[5]),
.mux_input_6(reg_outputs[6]),
.mux_input_7(reg_outputs[7]),
.mux_output(Out_1)
);

endmodule