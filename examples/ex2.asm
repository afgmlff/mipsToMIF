.text
LABEL:
bne $t1, $zero, LABEL1
LABEL1:
beq $t1, $zero, LABEL2
LABEL2:
bgez $t1, LABEL3
LABEL3:
bgezal $t1, LABEL4
LABEL4:
j LABEL5
LABEL5:
jal LABEL6
LABEL6:
add $t0, $t1, $t1

.data

