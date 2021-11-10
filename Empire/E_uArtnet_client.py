import socket
import _thread

class E_uArtnet_client:
    '''Ultra simple Art-Net client 
    
    Dependent of render module, needs a callback
    Ignore all cheks and just push 1st 4 values in 1st DMX universe onto the LEDs
    '''
    
    
    def __init__(self, callback, start=0, length=4, debug=False):
        self._callback = callback
        self._start = start
        self._end = length
        self._debug = debug
        # to exit _thread
        self._die = False
        
        # TODO check if inet is up
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self._socket.bind((sta_if.ifconfig()[0],6454))
        self._socket.bind(("0.0.0.0",6454))
        #self._sock.setblocking(False)

        _thread.start_new_thread(self.udp_reader_loop,())
        print("ArtNet: started")

    def udp_reader_loop(self):
        if self._die:
            print("ArtNet: exit")
            _thread.exit()
            
        while True:
            try:
                data, addr = self._socket.recvfrom(1024)
                # check if it is an artnet packet
                if len(data) > 20:
                    # data integrity checking
                    AN_header = data[0:7]
                    AN_opcode = data[8:10]
                    AN_length = data[17]
                    AN_universe = data[14:16]
                    
                    check_state = 0
                    # check packet type
                    if AN_header == b"Art-Net":
                        check_state = 1
                    # check if it is artnet light package (Opcode ArtDMX (0x5000) little endian)
                    if AN_opcode == b'\x00P' and check_state == 1:
                        check_state = 2
                    # check universe number
                    if AN_universe == b'\x00\x00' and check_state == 2:
                        check_state = 99
                    
                    # check that we would not try to read data beyon the end of the pacet
                    if check_state == 99:
                        dataStart = 18+self._start
                        dataEnd = 18+self._start+self._end
                        self._callback(data[dataStart:dataEnd])
                        
                if self._debug:
                    self._data = data
                    
            except Exception as e:
                print(e)