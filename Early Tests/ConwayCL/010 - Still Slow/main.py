import pyopencl as cl
import numpy as np
import random as r
import datetime as date
import time 

np.set_printoptions(threshold=np.nan)

class CL:
	def __init__(self):
		self.ctx = cl.create_some_context()
		self.queue = cl.CommandQueue(self.ctx)
		self.tick = False

	#Load kernal file and load as internal program
	def loadProgram(self, filename):
		#read in the OpenCL source file as a string
		f = open(filename, 'r')
		fstr = "".join(f.readlines())
		#print fstr
		#create the program
		self.program = cl.Program(self.ctx, fstr).build()

	#Create the host structures and buffers
	def popCorn(self):
		mf = cl.mem_flags
		
		#initialize client side (CPU) arrays
		#Use ar_ySize to increase the worldspace
		self.ar_ySize = np.int32(36)
		self.a = np.ones((self.ar_ySize,self.ar_ySize), dtype=np.int32)
		self.c = np.ones((self.ar_ySize,self.ar_ySize), dtype=np.int32)
		#create OpenCL buffers
		self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.a)
		self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.a.nbytes)

	#Run Kernal, create buffer, fill buffer
	def execute(self):
		self.program.Conway(self.queue, self.a.shape, None, self.ar_ySize, self.a_buf, self.dest_buf)
		cl.enqueue_read_buffer(self.queue, self.dest_buf, self.a).wait()
		
		#Refresh buffers
		mf = cl.mem_flags
		self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.a)

	#Seed, fill buffer
	def seed(self):
		np.random.seed(r.randint(0,100000))
		self.a = np.int32(np.random.randint(2, size=(self.ar_ySize, self.ar_ySize)))

		#Refresh buffers
		mf = cl.mem_flags
		self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.a)

	#Print the output array
	def render(self):
		print self.a
	
if __name__ == "__main__":
	example = CL()
	example.loadProgram("kTest.cl")
	example.popCorn()
	example.seed()	

	#Diagnostics
	iterations = 1000
	total_cells = iterations*example.ar_ySize*example.ar_ySize
	print "task:", example.ar_ySize, "x", example.ar_ySize, "for", iterations, "iterations,", total_cells, "total cells"

	#Run the loop
	time1=time.clock()
	for i in range(iterations):
		example.execute()
	time2=time.clock()
	
	#Results
	print "GPU time:", total_cells, "cells in", unicode(time2-time1), "sec"
	print "Cells per Second:", (total_cells/(time2-time1))
	
	# WARNING: SLOW
	if example.ar_ySize <= 100:
		print "Begin CPU Render"
		example.render()
	else:
		print "Array size must be <= 100 to attempt a terminal render"



