module piso #(
    parameter INPUT_SIZE = 256,
    parameter OUTPUT_SIZE = 64
)
(
    input wire clk,
    input wire ce,
    input wire rst,

    input wire [INPUT_SIZE-1:0] i_parallel,
    output wire [OUTPUT_SIZE-1:0] o_serial,
    
    input wire      fifo_empty,
    output wire     fifo_re,

    output wire     valid
);

// module that interface a fifo that contains parallel data
//that we wish to serialize.
//note that for each value that we read from the fifo we need 
// INPUT_SIZE/OUTPUT_SIZE cycles until we could read the next val

parameter CYCLES_BTW = INPUT_SIZE/OUTPUT_SIZE; 

parameter IDLE = 2'b0;
parameter BUSY = 2'b1;



reg [$clog2(CYCLES_BTW)-1:0] counter=0;
reg re, valid_r; //read enable and valid..

reg state=IDLE, next_state=IDLE;


always@(posedge clk)begin
    if(rst)
        state <= IDLE;
    else
        state <= next_state;
end


always@(*)begin
    case(state)
        IDLE:   begin
            if(~fifo_empty)     next_state = BUSY;
            else                next_state = IDLE;
        end
        BUSY:   begin
            if(counter==(CYCLES_BTW)-1) next_state = IDLE;
            else                        next_state = BUSY;
        end
    endcase 
end

always@(posedge clk)begin
    case(state)
        IDLE: begin
            counter<=0;
            valid_r <= 0;
        end
        BUSY: begin
            valid_r<= 1;
            counter <= counter +1;
        end
    endcase
end


always@(posedge clk)begin
    re = ~state && next_state && ~rst;
end

//detect the transition of states
assign fifo_re = re; 


reg [OUTPUT_SIZE-1:0] serial_out;


always@(*)begin
    case(counter)
        1: serial_out = i_parallel[OUTPUT_SIZE-1:0];
        2: serial_out = i_parallel[2*OUTPUT_SIZE-1:1*OUTPUT_SIZE];
        3: serial_out = i_parallel[3*OUTPUT_SIZE-1:2*OUTPUT_SIZE];
        0: serial_out = i_parallel[4*OUTPUT_SIZE-1:3*OUTPUT_SIZE];
    endcase
end


/*
always@(*)begin
    integer i;
    for(i=0; i<CYCLES_BTW;i=i+1)begin: loop
        if(counter==i)begin
            serial_out = i_parallel[(i+1)*OUTPUT_SIZE-1:i*OUTPUT_SIZE];
        end
    end
end
*/

assign valid = valid_r;
assign o_serial = serial_out; 
endmodule 
