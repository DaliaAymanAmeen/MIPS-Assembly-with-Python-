vsim work.mipsfinal7
run 10000000
mem save -o ins.txt -f mti -data decimal -addr decimal -wordsperline 1 /mipsfinal7/mips/inst_mem/instruction_memory
mem save -o reg.txt -f mti -data decimal -addr decimal -wordsperline 1 /mipsfinal7/mips/regfile/register
mem save -o data.txt -f mti -data decimal -addr decimal -wordsperline 1 /mipsfinal7/mips/data20/MEMO
quit
