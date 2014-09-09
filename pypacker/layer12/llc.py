from pypacker import pypacker
import struct

LLC_TYPE_IP		= 0x0800		# IPv4 protocol
LLC_TYPE_ARP		= 0x0806		# address resolution protocol
LLC_TYPE_IP6		= 0x86DD		# IPv6 protocol


class LLC(pypacker.Packet):
	__hdr__ = (
		("dsap", "B", 0),
		("ssap", "B", 0),
		("ctrl", "B", 0),
		("snap", "5s", "\x00" * 5),
	)

	def _dissect(self, buf):
		#dsap = struct.unpack("B", buf[0])[0]

		if buf[0] == 170:		# = 0xAA
		# SNAP is following ctrl
			type = struct.unpack("H", buf[5:7])[0]
			self._parse_handler(type, buf[8:])
		else:
		# deactivate SNAP
			self.snap = None


# load handler
from pypacker.layer12 import arp
from pypacker.layer3 import ip, ip6

pypacker.Packet.load_handler(LLC,
	{
		LLC_TYPE_IP: ip.IP,
		LLC_TYPE_ARP: arp.ARP,
		LLC_TYPE_IP6: ip6.IP6,
	}
)
