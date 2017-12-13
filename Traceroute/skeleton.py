#!/usr/bin/python

import optparse
import socket
import sys
import time
import math

icmp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')

def create_sockets(ttl):
    """
    Sets up sockets necessary for the traceroute.  We need a receiving
    socket and a sending socket. 
    """
	#Your code here
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)

    """
    Set socket options and timeout value for the recv socket
    """
    #Your code here
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    return recv_socket, send_socket

def main(dest_name, port, max_hops,timeout):
    dest_addr = socket.gethostbyname(dest_name)
    ttl = 1
    while True:

        rtt = [1,2,3]
        i=0

        for i in range(0,3):
            recv_socket, send_socket = create_sockets(ttl)
            recv_socket.bind(("", port))
            send_socket.sendto("", (dest_name, port))

            """
            Record the current time
            """
            #Your code here
            curr_time = time.time()

            curr_addr = None
            curr_name = None
            try:
                # socket.recvfrom() gives back (data, address), but we
                # only care about the latter.
                _, curr_addr = recv_socket.recvfrom(512)
                curr_addr = curr_addr[0]  # address is given as tuple

                """
    	        Compute the round trip time
                """
                #Your code here
                roundTrip = (time.time() - curr_time)*1000
                rtt[i]=roundTrip
                i=i+1
                try:
                    curr_name=socket.gethostbyaddr(curr_addr)[0]
                except:
                    curr_name=curr_addr

            
            except socket.timeout:
                """
      	        Handle time out 
                """
                #Your code here
                print("Time Out")
                ttl+=1
                send_socket.sendto("", (dest_name, port))
                pass
            except socket.error:
                pass
            finally:
                send_socket.close()
                recv_socket.close()

            if curr_addr is not None:
    	        """
    	        Print out necessary information as the following example
    			5  xe-2-2-0.tor10.ip4.gtt.net (77.67.69.237)  12.321 ms
    	        """
    	        #Your code here
    	        avg = sum(rtt)/len(rtt)
    	        std = math.sqrt(((rtt[0]-avg)**2+(rtt[1]-avg)**2+(rtt[2]-avg)**2)/3)


    	        print "%d\t%s (%s)\t%.3f ms\t%.3f ms\t%.3f ms\t avg:%.3f ms\t std: %.3f ms" % (ttl, curr_name, curr_addr, rtt[0],rtt[1],rtt[2],avg,std)
    	        ttl += 1
            else:
    	        """
    	        Print out ttl and *
    	        """
    	        #Your code here
    	        curr_host = '*'
    	        print "%d\t%s" % (ttl, curr_host)




        if curr_addr == dest_addr or ttl > max_hops:
            break
        
    return 0

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="%prog [options] hostname")
    parser.add_option("-p", "--port", dest="port",
                      help="Port to use for socket connection [default: %default]",
                      default=33434, metavar="PORT")
    parser.add_option("-m", "--max-hops", dest="max_hops",
                      help="Max hops before giving up [default: %default]",
                      default=30, metavar="MAXHOPS")
    """
 	Add an option of timeout value; default value is 5 second
    """
    #Your code here
    parser.add_option('-w', '--timeout', dest='timeout',
                      help = 'Timeout Value in s [default: %default]', default = 5,
                      metavar = 'TIMEOUT')

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("No destination host")
    else:
        dest_name = args[0]

    """
	Modify the following to include an argument to store the timeout value
    """
	#Change the following line
    sys.exit(main(dest_name=dest_name,
                  port=int(options.port),
                  max_hops=int(options.max_hops),
                  timeout = int(options.timeout)))
