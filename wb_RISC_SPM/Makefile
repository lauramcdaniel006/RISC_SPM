# COCOTB variables
export COCOTB_REDUCED_LOG_FMT=1
export PYTHONPATH := test:$(PYTHONPATH)
export LIBPYTHON_LOC=$(shell cocotb-config --libpython)

all: test_wishbone

test_wishbone:
	rm -rf sim_build/ results.xml
	mkdir sim_build/
	iverilog -o sim_build/sim.vvp -s wb_RISC_SPM -s dump -g2012 wb_RISC_SPM.v dump_wb.v

	MODULE=test_wb vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	! grep failure results.xml

show:
	gtkwave wb_RISC_SPM.vcd wb_RISC_SPM.gtkw

clean:
	rm -rf *vcd sim_build __pycache__ results.xml

.PHONY: clean
