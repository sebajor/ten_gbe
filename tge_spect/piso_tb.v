module piso_tb;
    parameter INPUT_SIZE = 256;
    parameter OUTPUT_SIZE = 64;


    reg  clk;
    reg  ce;
    reg  rst;

    reg  [INPUT_SIZE-1:0] i_parallel;
    wire  [OUTPUT_SIZE-1:0] o_serial;
    
    reg       fifo_empty;
    wire      fifo_re;

    wire      valid;


piso #( 
    .INPUT_SIZE(INPUT_SIZE),
    .OUTPUT_SIZE(OUTPUT_SIZE)
) piso (
    .clk(clk),
    .ce(ce),
    .rst(rst),
    .i_parallel(i_parallel),
    .o_serial(o_serial),
    .fifo_empty(fifo_empty),
    .fifo_re(fifo_re),
    .valid(valid)
);


initial begin
    clk = 0;
    ce = 1;
    rst = 0;
    i_parallel = {{64'd0, 64'd1}, {64'd2, 64'd3}};
    fifo_empty = 1;
end


parameter HALF_PERIOD =  5;
parameter PERIOD = 10;

always
    #HALF_PERIOD clk = ~clk;


initial begin
    $dumpfile("piso.vcd");
    $dumpvars();
end

initial begin
    rst = 1;
    #(3*PERIOD);
    rst = 0;
    #(10*PERIOD);
    fifo_empty = 0;
    #(30*PERIOD);
    $finish;
end


endmodule 
