import pyopencl as cl
import numpy
numpy.set_printoptions(threshold=numpy.nan)

class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def loadProgram(self, filename):
        #read in the OpenCL source file as a string
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        print fstr
        #create the program
        self.program = cl.Program(self.ctx, fstr).build()

    def popCorn(self):
        mf = cl.mem_flags

        #initialize client side (CPU) arrays
        self.a = numpy.ones((5,5), dtype=numpy.int32)

        #create OpenCL buffers
        self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.a)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.a.nbytes)

    def execute(self):
        self.program.part1(self.queue, self.a.shape, None, self.a_buf, self.dest_buf)
        print "a", self.a    
        c = numpy.zeros_like(self.a)
        print "PRE-c", c
        cl.enqueue_read_buffer(self.queue, self.dest_buf, c).wait()
        print "c", c



if __name__ == "__main__":
    example = CL()
    example.loadProgram("part1.cl")
    example.popCorn()
    example.execute()

