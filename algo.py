# Author: David Alan Lariviere

#!/usr/bin/env python 
import sys 
import struct 
unpack = struct.unpack 
structerror = struct.error 
import datetime

# For references: 
# ftp://ftp.cmegroup.com/SBEFix/NRCert/Templates/templates_FixBinary.xml 
# http://www.cmegroup.com/confluence/display/EPICSANDBOX/MDP3

# Note inside base_path are N files numbered 0.dat ­­--> 2000.dat 
base_path = "/mnt/vmshared/data/mdp3_data"

class MDP3Parser: 
	# def __init__(self):

	# Given a byte describing the match event, create a string describing its contents: see reference 
	# @ http://www.cmegroup.com/confluence/display/EPICSANDBOX/MDP3+­+Market+ Data+Incremental+Refresh under tag 5799 
	def match_event_string(self, match_event_byte): 
		desc = "" 
		# Bit 0: (least significant bit) Last Trade Summary message for a given event 
		# Bit 1: Last electronic volume message for a given event 
		# Bit 2: Last real quote message for a given event 
		# Bit 3: Last statistic message for a given event 
		# Bit 4: Last implied quote message for a given event 
		# Bit 5: Message resent during recovery 
		# Bit 6: Reserved for future use 
		# Bit 7: (most significant bit) Last message for a given event 
		if match_event_byte & 1:
			desc = desc + " last trade for event |" 
		if match_event_byte & 2:
			desc = desc + " last volume | " 
		if match_event_byte & 4: 
			desc = desc + " last quote | "
		if match_event_byte & 8:
			desc = desc + " last quote | " 
		if match_event_byte & 16:
			desc = desc + " last implied quote | " 
		if match_event_byte & 32:
			desc = desc + " resent during recovery |" 
		if match_event_byte & 64:
			desc = desc + " reserved for future use | " 
		if match_event_byte & 128: 
			desc = desc + " last msg of an event | "
		return desc

	def parse_file(self, filename): 
		self.seenbytes = 0 
		self.prevbytes = 0 
		f = file(filename)
		num_bytes_to_read = 16 
		nbytes = f.read() 
		print "Will parse", cur_msg_filename, "\t contains ", len(nbytes), " bytes"
		# print "\tRaw Frame: ", ':'.join(x.encode('hex') for x in nbytes) 
		# 	print ' '.join('{:02x}'.format(x) for x in nbytes)
		# TODO: replace so we can handle parsing multiple messages
		# All MDP messages start with "binary packet header" consists of:
		# 	MsgSeqNum: uint32 
		# 	SendingTime: uint64 
		msg_seq_num, raw_epoch_sending_time_ns = unpack('<IQ', nbytes[:12])
		sending_datetime = datetime.datetime.fromtimestamp(raw_epoch_sending_time_ns / 1000000000)
		print "\tBinary Packet Header: Seq Num / Epoch NS Timestamp: ", msg_seq_num, "\t", raw_epoch_sending_time_ns, "\t", sending_datetime, ".", (raw_epoch_sending_time_ns % 1000000000)
		nbytes = nbytes[12:] # drop the header bytes
		# Message header: 
		# 	MsgSize: uint16 
		# 	BlockLength: uint16 
		# 	TemplateID: uint16 
		# 	SchemaID: uint16 
		# 	note typo on website? last two listed as i 16s but each only one byte long 
		# 	Version: uint16 
		msg_size, block_length, template_id, schema_id, version = unpack('<HHHBB', nbytes[:8]) 
		print "\tMsg Size: ", msg_size 
		print "\tBlock Length: ", block_length 
		print "\tTemplate ID: ", template_id 
		print "\tSchema ID: ", schema_id 
		print "\tVersion: ", version
		nbytes = nbytes[8:] #drop the message header bytes
		# FIX Message Header: 
		# MsgType: "int" is this 4 bytes or not? 
		# fix_msg_type = unpack('<i', nbytes[:4]) 
		# print "\tRemaining bytes: ", nbytes 
		# print "\tFix Msg Type: ", fix_msg_type
		# right now, only implementing parsing for template 20 
		if template_id != 20: 
			return

		# Note: 
		# 	<ns2:message name="MDIncrementalRefreshBook" id="20" description="MDIncrementalRefreshBook" blockLength="9" semanticType="X"> 
		# 	<field name="TransactTime" id="60" type="uInt64" description="Start of event processing time in number of nanoseconds since Unix epoch" offset="0" semanticType="UTCTimestamp"/> 
		# 	<field name="MatchEventIndicator" id="5799" type="MatchEventIndicator" description="Bitmap field of eight Boolean type indicators reflecting the end of updates for a given Globex event" offset="8" semanticType="MultipleCharValue"/>
		# 	<group name="NoMDEntries" id="268" description="Number of entries in Market Data message" blockLength="27" dimensionType="groupSize"> 
		# 	<field name="MDUpdateAction" id="279" type="MDUpdateAction" description=" Market Data update action" offset="0" semanticType="int"/> 
		# 	<field name="MDEntryType" id="269" type="MDEntryTypeBook" description="Market Data entry type " offset="1" semanticType="char"/> 
		# 	<field name="SecurityID" id="48" type="Int32" description="Security ID" offset="2" semanticType="int"/> 
		# 	<field name="RptSeq" id="83" type="Int32" description="Market Data entry sequence number per instrument update" offset="6" semanticType="int"/> 
		# 	<field name="MDPriceLevel" id="1023" type="uInt8" description="Aggregate book level" offset="10" semanticType="int"/> 
		# 	<field name="MDEntryPx" id="270" type="PRICENULL" description="Market Data entry price" offset="11" semanticType="Price"/> 
		# 	<field name="MDEntrySize" id="271" type="Int32NULL" description="Market Data entry quantity" offset="19" semanticType="Qty"/> 
		# 	<field name="NumberOfOrders" id="346" type="Int32NULL" description="In Book entry ­ aggregate number of orders at given price level" offset="23" semanticType="int"/> 
		# 	</group> 
		# 	</ns2:message> 
		# 	print ".join("{:02x}".format(ord(c)) for c in nbytes) 
			# print "\t", ':'.join(x.encode('hex') for x in nbytes) 
			# note "NoMDEntries" is a composite type defined as uint16 blockLength + uin8 numInGroup
		raw_transact_time_ns, match_event_indicator, block_length, num_md_entries = unpack("<QBHB", nbytes[:12]) 
		print "\tRaw Transact Time NS: ", raw_transact_time_ns 
		print "\tMatch Event Indicator: ", match_event_indicator, "\t", self.match_event_string(match_event_indicator) 
		print "\tNum MD Entries: ", num_md_entries 
		num_bytes_left = (len(nbytes) - 12) 
		if num_md_entries > 0: 
			print "\tNOTE: have ", num_bytes_left, " bytes of repeating groups: averaging ", (num_bytes_left / num_md_entries), " bytes per entry" 
			nbytes = nbytes[12:]
		if num_md_entries > 0 and len(nbytes) < 27: 
			print "Error: invalid sized byte array of only ", len(nbytes), "; skipping!" 
			return

		cur_entry = 0

		while len(nbytes) >= 27: 
			# Begin repeating group of entries 
			update_action, entry_type, security_id, rpt_seq, price_level, entry_price_mantissa, entry_size, num_orders = unpack("<BcIiBqii", nbytes[:27]) 
			entry_price_exponent = ­7 # hard coded constant 
			entry_price = entry_price_mantissa * pow(10, entry_price_exponent) 
			# note for implied liquidity, there is no concept of # of orders, so field can be null, represented as all 1's except highest bit (2147483647 in base 10) 
			if num_orders == 2147483647:
				num_orders = "NULL" 
				#print "\tRaw Bytes for Entry", ':'.join(x.encode('hex') for x in nbytes) 
				print "\t", cur_entry, " entry message: " 
				print "\t\tUpdate Action: ", update_action 
				print "\t\tEntry Type: ", entry_type 
				print "\t\tSecurity ID: ", security_id 
				print "\t\tRpt Seq: ", rpt_seq 
				print "\t\tPrice Level: ", price_level 
				print "\t\tEntry Price Mantissa: " , entry_price_mantissa 
				print "\t\tEntry Price Exponent: ", entry_price_exponent 
				print "\t\tEntry Price: ", entry_price 
				print "\t\tEntry Size: " , entry_size 
				print "\t\tNum Orders: ", num_orders 
				cur_entry = cur_entry + 1 nbytes = nbytes[27:] 
			# if not nbytes: 
			#	yield (None, 'EOF at %d' % self.seenbytes) 
			#	break 
			#	self.seenbytes += num_bytes_to_read 
			#	print ''.join('{:02x}'.format(x) for x in nbytes)
			# length = unpack('>H', nbytes)[0]

parser = MDP3Parser()
for i in range(2000): 
  cur_msg_filename = base_path + "/%d.dat" % (i) 
	parser.parse_file(cur_msg_filename)
