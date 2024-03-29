"""
test wishbone peripheral
"""

import cocotb
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotbext.wishbone.driver import WishboneMaster, WBOp

# from J Pallent: 
# https://github.com/thejpster/zube/blob/9299f0be074e2e30f670fd87dec2db9c495020db/test/test_zube.py
async def test_wb_set(wbs, addr, value):
    """
    Test putting values into the given wishbone address.
    """
    await wbs.send_cycle([WBOp(addr, value)])

async def test_wb_get(wbs, addr):
    """
    Test getting values from the given wishbone address.
    """
    res_list = await wbs.send_cycle([WBOp(addr)])
    rvalues = [entry.datrd for entry in res_list]
    return rvalues[0]

async def rst(dut):
    dut.rst = 0  
    dut.i_wb_data = 0
    await ClockCycles(dut.clk, 5)
    dut.rst = 0
    await ClockCycles(dut.clk, 5)

@cocotb.test()
async def test_all(dut):
    """
    Run all the tests
    """
    clock = Clock(dut.clk, 10, units="us")

    cocotb.fork(clock.start())

    signals_dict = {
        "cyc":  "i_wb_cyc",
        "stb":  "i_wb_stb",
        "we":   "i_wb_we",
        "adr":  "i_wb_addr",
        "datwr":"i_wb_data",
        "datrd":"o_wb_data",
        "ack":  "o_wb_ack"
    }
    wbs = WishboneMaster(dut, "", dut.clk, width=32, timeout=10, signals_dict=signals_dict)

    await rst(dut)
    
    #after this line code changes
    
    # Set up our memory addresses for both sides
    input_addr = 0x3000_0000
    output_addr = 0x3000_0004

    # input
    #data = await test_wb_get(wbs, input_addr)
    #assert data == BinaryValue('00000000')

    # set inputs and check they're correct
    await test_wb_set(wbs, input_addr, BinaryValue('1111111111111111'))
    data = await test_wb_get(wbs, input_addr)
    assert data == BinaryValue('1111111111111111')

    # rst the system for the next test
    await rst(dut)
    
    # output
    result = await test_wb_get(wbs, output_addr)
   #* assert result == 0

    # check if logic works

    dut.data_bus = BinaryValue('10000001')
    dut.address_bus = BinaryValue('00000001')
    dut.memory_bus = await test_wb_get(wbs, output_addr)
    dut.instruction_bus = await test_wb_get(wbs, output_addr)
    #* assert result == BinaryValue('10000010')

    await rst (dut)
