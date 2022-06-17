import sys
sys.path.append('../lib')

import os
from pymodbus.constants     import Endian
from pymodbus.payload       import BinaryPayloadDecoder
from pymodbus.client.sync   import ModbusSerialClient as ModbusClient
from configparser import ConfigParser


class   Px2Config:
    __slots__       =   'adc_bits', 'adc_vref_mv', 'adc_mV_per_bit'

###############################################################################
# CALLBACK
class Px2:

    def __init__(self, port, baud=9600, addr=0):
        self.modbus_addr = addr
        self.client = ModbusClient(method='rtu', port=port, baudrate=baud, timeout=1)

    def get_meas( self ):
        self.client.connect()
        raw = self.client.read_holding_registers( address=0x0014, count=21, unit=self.modbus_addr ) 

        if raw.isError():
            data    = None
        else:
            data    = raw
            obj     = BinaryPayloadDecoder.fromRegisters(raw.registers, byteorder=Endian.Big)
            data    = { 'hreg_20':          obj.decode_16bit_uint(),
                        #'hreg_21':          obj.decode_32bit_float(),
                        #'hreg_23':          obj.skip_bytes(4),
                        #'hreg_30':          obj.decode_32bit_uint(),
                        'hreg_21':          obj.decode_16bit_int(),
                        'hreg_22':          obj.decode_16bit_int(),
                        'hreg_23':          obj.decode_16bit_int(),
                        'hreg_24':          obj.decode_16bit_int(),
                        'hreg_25':          obj.decode_16bit_uint(),
                        'hreg_26':          obj.decode_16bit_uint(),
                        'hreg_27':          obj.decode_16bit_uint(),
                        'hreg_28':          obj.decode_16bit_uint(),
                        'hreg_29':          obj.decode_16bit_int(),
                         'ticker':          obj.decode_16bit_int(),
                        'hreg_31':          obj.decode_16bit_int(),
                        'hreg_32':          obj.decode_16bit_int(),
                        'hreg_33':          obj.decode_16bit_int(),
                        #'hreg_34':          obj.decode_16bit_uint(),
                        #'hreg_35':          obj.decode_16bit_uint(),
                        'hreg_3435':        obj.decode_32bit_uint(),

                        #'hreg_36':          obj.decode_16bit_uint(),
                        #'hreg_37':          obj.decode_16bit_uint(),
                        'hreg_3637':        obj.decode_32bit_uint(),

                        'hreg_38':          obj.decode_16bit_uint(),
                        'hreg_39':          obj.decode_16bit_uint(),
                         'status':          obj.decode_16bit_uint(),
            }

        #print(raw.registers)

        self.client.close()

        return data



###############################################################################
# MAIN
if __name__ == '__main__':

    #import os
    from os import system, name
    import time

    name, _ = os.path.splitext(os.path.basename(__file__))
    conf    = ConfigParser()
    conf.read( name + '.ini' )
    port    = conf.get(     'MODBUS',   'port'      )
    baud    = conf.getint(  'MODBUS',   'baudrate'  )
    addr    = conf.getint(  'MODBUS',   'address'   )
    px2     = Px2(port, baud, addr)

    #print( '-' * 80 )
    #print( 'NAME\t\tTYPE\tUNIT\tMEAS\t\tSTATUS\t\tFACTOR\tOFFSET' )
    #print( '-' * 80 )

    try:
        with open( name+'.log.txt', 'w' ) as f:
            d = px2.get_meas()
            #print(d)
            for key in d:
                f.write( str(key) + ',' )
            f.write('\r')

            while( True ):
                d = px2.get_meas()
                if d != None:
                    system('cls')
                    #print (u"{}[2J{}[;H".format(chr(27), chr(27)))
                    #print("\033c")
                    #sys.stderr.write("\x1b[2J\x1b[H")
                    #print('\x0c')
                    #print(chr(27) + "[2J")
                    #print( ' CONCENTRATION: %.2f PPM'   % d['concentration']    )
                    #print( '   TEMPERATURE: %.2f mV'    % d['temperature']      )
                    #print( '      PRESSURE: %.2f hPa'   % d['pressure']         )
                    #print( '       ADC RAW: %08X'       % d['adc raw']          )
                    print('       hreg_20:     %04Xh %d' % ( d['hreg_20'], d['hreg_20'])          )
                    print('       hreg_21:     %04Xh %d' % ( d['hreg_21'], d['hreg_21'])          )
                    print('       hreg_22:     %04Xh %d' % ( d['hreg_22'], d['hreg_22'])          )
                    print('       hreg_23:     %04Xh %d' % ( d['hreg_23'], d['hreg_23'])          )
                    print('       hreg_24:     %04Xh %d' % ( d['hreg_24'], d['hreg_24'])          )
                    print('       hreg_25:     %04Xh %d' % ( d['hreg_25'], d['hreg_25'])          )
                    print('       hreg_26:     %04Xh %d' % ( d['hreg_26'], d['hreg_26'])          )
                    print('       hreg_27:     %04Xh %d' % ( d['hreg_27'], d['hreg_27'])          )
                    print('       hreg_28:     %04Xh %d' % ( d['hreg_28'], d['hreg_28'])          )
                    print('       hreg_29:     %04Xh %d' % ( d['hreg_29'], d['hreg_29'])          )
                    print('        ticker:     %04Xh %d' % ( d['ticker'],  d['ticker'])           )
                    print('       hreg_31:     %04Xh %d' % ( d['hreg_31'], d['hreg_31'])          )
                    print('       hreg_32:     %04Xh %d' % ( d['hreg_32'], d['hreg_32'])          )
                    print('       hreg_33:     %04Xh %d' % ( d['hreg_33'], d['hreg_33'])          )

                    #print('       hreg_34: %04Xh %d'         % ( d['hreg_34'], d['hreg_34'])          )
                    #print('       hreg_35: %04Xh %d'         % ( d['hreg_35'], d['hreg_35'])          )
                    print('     hreg_3435: %08Xh %d' % ( d['hreg_3435'], d['hreg_3435'])          )

                    #print('       hreg_36:     %04Xh %d' % ( d['hreg_36'], d['hreg_36'])          )
                    #print('       hreg_37:     %04Xh %d' % ( d['hreg_37'], d['hreg_37'])          )
                    print('     hreg_3637: %08Xh %d' % ( d['hreg_3637'], d['hreg_3637'])          )

                    print('       hreg_38:     %04Xh %d' % ( d['hreg_38'], d['hreg_38'])          )
                    print('       hreg_39:     %04Xh %d' % ( d['hreg_39'], d['hreg_39'])          )
                    #print( '        status: %04Xh'         % ( d['status']               )          )
                    #print('        status: %04Xh {:016b}b'.format(d['status']) % d['status']                      )
                    #print('        status: %04Xh %0b' % (d['status'], d['status'])            )
                    print('        status:     {0:04X}h {0:016b}b'.format(d['status']) )


                #f.write( str(d['hreg_20']) + str(d['hreg_21']) )
                for idx in d:
                    f.write( str(d[idx]) + ',' )
                f.write('\r')

                time.sleep(1)
    except KeyboardInterrupt:
        print('\n\rDone')
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
