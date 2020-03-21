
`timescale 1ns/1ps

module MIPSY(input clk);
wire branch,jump,zero,jr,jal,memtoreg,memwrite,memread,regwrite,alusrc,and_branch ;
wire[1:0] regdst,aluop;
wire[31:0] inst,pcin,pc_4,pcout,mux5_reg,data1,data2,signexout,mux6_alu,alu_data,data_mux4,mux4_mux5,add2_mux1,mux1_mux2,mux2_mux3,shift_mux2;
wire [3:0] alucontrolout;
wire [4:0] mux7_reg;
reg[4:0] constant=31;




clockgen  c1(clk);

InsturctionMemory inst_mem(pcout,inst);

RegisterFile regfile(inst[25:21],inst[20:16],mux7_reg,mux5_reg,regwrite,data1,data2);

MUX3in mux7(mux7_reg,inst[20:16],inst[15:11],constant,regdst);

signextend signex(signexout,inst[15:0]);

ALU_control aluctr(alucontrolout,aluop,inst[5:0],jr);


ALU alu(alucontrolout,data1,mux6_alu,inst[10:6],alu_data,zero,clk);

MUX mux6(mux6_alu,data2,signexout,alusrc);

data_memory data20(alu_data,data2,memwrite,memread,data_mux4);

MUX mux4(mux4_mux5,alu_data,data_mux4,memtoreg);

MUX mux5(mux5_reg,mux4_mux5,pc_4,jal);


controlunit5 controlunit( regdst,jump,branch,memread,memtoreg,aluop,memwrite,alusrc,regwrite,jal ,inst[31:26]);

MUX mux1(mux1_mux2,pc_4,add2_mux1,and_branch);

MUX mux2(mux2_mux3,mux1_mux2,shift_mux2,jump);


MUXpc mux3(pcin,mux2_mux3,data1,jr);

pc pc1(pcout,pc_4,pcin,clk);






assign a=2'b00;
assign add2_mux1 = pc_4+ ({a,signexout});


assign shift_mux2 = {pc_4[31:28],a,inst[25:0]};




and (and_branch,branch,zero);

initial
begin
$monitor("=%d pout   - %d  inst   - %d  Data1   - %d  Data2  - %d alu_data -%d writereg %d add2_mux1 %d pcin   %d mux2_mux3 ",pcout,inst,data1,data2,alu_data,mux5_reg,add2_mux1, pcin, mux2_mux3);
end


endmodule


module MUXpc(o1,in1,in2,sel);
output reg [31:0] o1;
input [31:0] in1,in2;
input sel;
initial 
begin 
o1<=32'b0000_0000_0000_0000_0000_0000_0000_0000;
end

always@(in1,in2,sel)
begin
if(sel==0)
o1<=in1;
else if(sel==1)
o1<=in2;
else
o1<=32'b0000_0000_0000_0000_0000_0000_0000_0000;
end

endmodule
module ALU_control(ALUctr,ALUop,funct,jr);
input[1:0] ALUop;
input[5:0] funct;
output reg [3:0] ALUctr;
output reg jr;

always @(ALUop,funct)
case(ALUop)
2'b00: begin ALUctr<=4'b0010; jr<=0; end
2'b01: begin ALUctr<=4'b0110; jr<=0; end
2'b11: begin ALUctr<=4'b0001; jr<=0; end
2'b10:
 case(funct)
6'b100000: begin ALUctr<=4'b0010;  jr<=0; end 
6'b100010: begin ALUctr<=4'b0110;  jr<=0; end
6'b100100: begin ALUctr<=4'b0000;  jr<=0; end
6'b100101: begin ALUctr<=4'b0001;  jr<=0; end
6'b101010: begin ALUctr<=4'b0111;  jr<=0; end
6'b000000: begin ALUctr<=4'b1110;  jr<=0; end
6'b000000: begin ALUctr<=4'b1110;  jr<=0; end
6'b001000: begin ALUctr<=4'b0000;  jr<=1; end

default: begin ALUctr<=4'bxxxx;  jr<=0; end

endcase

default: begin ALUctr<=4'bxxxx;  jr<=0; end

endcase







endmodule 





module ALU(ALUctr,A,B,C,AlUout,zero ,clk);
input clk;
input[3:0] ALUctr;
input [31:0] A,B;
input [4:0] C;
output reg [31:0] AlUout;
output reg zero;
always@(AlUout)
begin

if (AlUout==0) 
begin 
zero=1;end
else 
zero=0;
end
 
always @(posedge clk)
 begin
#1
$display("%b ALUctr",ALUctr);
case (ALUctr)
4'b0000: AlUout<= A&B;
4'b0001: AlUout<=A|B;
4'b0010: AlUout<=A+B;
4'b0110: AlUout<=A-B;
4'b0111: AlUout<=A<B?1:0;
4'b1110: AlUout<=B<<C;




default: AlUout<=0;

endcase

end

endmodule






module clockgen(clk);
output reg clk;
initial
begin
clk=0;
end
always 
begin
#31.25
clk=~clk;
end
endmodule



module data_memory (
input wire [31:0] addr,          // Memory Address
input wire [31:0] write_data,    // Memory Address Contents
input wire memwrite, memread,
                  
output reg [31:0] read_data);     // Output of Memory Address Contents


reg [31:0] MEMO[0:8191];  
integer i;

initial begin
  read_data <= 0;
for (i = 0; i < 8192; i = i + 1) begin
    MEMO[i] = i;
end
end

always@(memwrite,memread,addr)  begin

if (memwrite == 1'b1) begin
 
   MEMO[addr] <= write_data;
end
if (memread == 1'b1) begin

  read_data <= MEMO[addr];
end
end
endmodule


module controlunit5( regdst,jump,branch,memread,memtoreg,aluop,memwrite,alusrc,regwrite,jal ,opcode);
output reg [1:0]regdst , aluop;
output reg jump,branch,memread,memtoreg,memwrite,alusrc,regwrite,jal;
input [5:0]opcode;
always@(*)
begin
case(opcode)
0 : 
begin
regdst <= 1;
jump <= 0;
branch <= 0; 
memread <= 1;
memtoreg <= 0; 
aluop <= 2; 
memwrite <= 0; 
alusrc <= 0;
regwrite <= 1; 
jal <= 0;
$display("R Type");
end

2 :
begin
regdst <= 0; 
jump <= 1;
branch <= 0; 
memread <= 0;
memtoreg <= 0; 
aluop <= 0; 
memwrite <= 0; 
alusrc <= 0;
regwrite <= 0; 
jal <= 0;
 $display("2 Type");
end
3 :
begin
regdst <= 2; 
jump <= 1;
branch <= 0; 
memread <= 0;
memtoreg <= 0; 
aluop <= 0; 
memwrite <= 0; 
alusrc <= 0;
regwrite <=1 ; 
jal <= 1;
 $display("3 Type");
end
4 :
begin
regdst <= 1; 
jump <= 0;
branch <= 1; 
memread <=0 ;
memtoreg <= 0; 
aluop <= 1; 
memwrite <=0 ; 
alusrc <= 0;
regwrite <= 0; 
jal <= 0;

 $display("4 Type");
end
8 :
begin
regdst <= 0; 
jump <= 0;
branch <=0 ; 
memread <=0 ;
memtoreg <=0 ; 
aluop <= 0; 
memwrite <= 0; 
alusrc <= 1;
regwrite <= 1; 
jal <= 0;
$display("8 Type");
end
13 :
begin
regdst <= 0; 
jump <= 0;
branch <= 0; 
memread <= 0;
memtoreg <= 0; 
aluop <= 3; 
memwrite <= 0; 
alusrc <= 1;
regwrite <= 1; 
jal <= 0;
$display("13 Type");
end
35 :
begin
regdst <= 0; 
jump <= 0;
branch <= 0; 
memread <= 1;
memtoreg <= 1; 
aluop <= 0; 
memwrite <= 0; 
alusrc <= 1;
regwrite <= 1; 
jal <= 0;
$display("35 Type");

end
43 :
begin
regdst <=0 ; 
jump <= 0;
branch <= 0; 
memread <= 0;
memtoreg <= 1; 
aluop <= 0; 
memwrite <= 1; 
alusrc <= 1;
regwrite <= 0; 
jal <= 0;
$display("43 Type");
end
endcase
end 
endmodule

module InsturctionMemory(address, instruction);
input  [31:0] address;

output reg [31:0] instruction;
reg [31:0] instruction_memory [0:8191];

initial
begin
$readmemb("Instmem.txt",  instruction_memory);
end
always@(address)
begin

instruction = instruction_memory[address];
end



endmodule 




module MUX(o1,in1,in2,sel);
output reg [31:0] o1;
input [31:0] in1,in2;
input sel;
always@(in1,in2,sel)
begin
if(sel==0)
o1=in1;
else if(sel==1)
o1=in2;
else
o1=1'bx;

end
endmodule


module MUX3in(o1,in1,in2,in3,sel);
output reg [31:0] o1;
input [31:0] in1,in2,in3;
input wire[1:0] sel;
always@(in1,in2,in3,sel)
begin
if(sel==2'b00)
o1=in1;
else if(sel==2'b01)
o1=in2;
else if (sel==2'b10)
o1=in3;
else
o1 = o1;

end
endmodule






module RegisterFile(Read1,Read2, WriteReg,WriteData,RegWrite,Data1,Data2);
input [4:0] Read1, Read2, WriteReg;
input [31:0] WriteData;
input RegWrite;
output  [31:0]Data1;
output [31:0] Data2;
reg [31:0] register [0:31];

initial 
begin 
$readmemb("regFile.txt",  register);
 $display("%b reg0",register[0] );
end

assign Data1= register[Read1];
assign  Data2= register[Read2];
always @(WriteData,WriteReg)
begin 
#1
$display("%b WriteData", WriteData);
if(RegWrite==1) begin
 register[WriteReg]=WriteData; end

end

endmodule





module signextend (o1,in1);

input [15:0] in1;
output reg [31:0] o1;
wire [15:0] w0 = 16'b0000000000000000;
wire [15:0] w1 = 16'b1111111111111111;

always@(in1)


if(in1[15] == 1'b0)
 o1 = {w0,in1};

else if (in1[15] == 1'b1)
 o1 = {w1,in1};
else
o1=32'bx;


endmodule







module pc(o1,o2,pcin,clk);
input clk ; 
input[31:0] pcin ;
output reg [31:0] o1 , o2 ;

always@(posedge clk)
begin 
o1 <= pcin ;
 o2 <= pcin + 1 ;   
end
endmodule







module mipsfinal7();


MIPSY mips(clk);


clockgen  c1(clk);


endmodule




