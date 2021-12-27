import math

class bititerator:
  def __init__(self, message):
    self.message = message
    self.n = 0

  def getNext(self, n):
    result = 0
    while n:
      c = math.floor(self.n / 4)
      b = 3 - self.n % 4

      result = result << 1
      result += (int(self.message[c], 16) >> b) & 1

      self.n += 1
      n -= 1
    return result

assert(bititerator("A").getNext(1) == 1)
assert(bititerator("7").getNext(1) == 0)
assert(bititerator("A").getNext(2) == 2)
assert(bititerator("A").getNext(4) == 10)

def parsePacket(it):
  version = it.getNext(3)
  type_id = it.getNext(3)
  value = None
  sub_packets = []
  if type_id == 4: # Literal value
    value = 0
    while True:
      value = value << 4
      next = it.getNext(1)
      value += it.getNext(4)
      if not next:
        break
  else: # Operator
    length_type_id = it.getNext(1)
    if length_type_id:
      nr_sub_packets = it.getNext(11)
      for n in range(nr_sub_packets):
        it, data = parsePacket(it)
        sub_packets.append(data)
    else:
      nr_bits_sub_packets = it.getNext(15)
      end = it.n + nr_bits_sub_packets
      while it.n < end:
        it, data = parsePacket(it)
        sub_packets.append(data)
  if value is not None:
    return (it, (version, type_id, value))
  else:
    return (it, (version, type_id, sub_packets))

def sum_versions(parsed_packet):
  version = parsed_packet[0]
  if parsed_packet[1] != 4:
    for p in parsed_packet[2]:
      version += sum_versions(p)
  return version

test_packet_1 = "8A004A801A8002F478"
test_packet_2 = "620080001611562C8802118E34"
test_packet_3 = "C0015000016115A2E0802F182340"
test_packet_4 = "A0016C880162017C3686B18A3D4780"
assert(sum_versions(parsePacket(bititerator(test_packet_1))[1]) == 16)
assert(sum_versions(parsePacket(bititerator(test_packet_2))[1]) == 12)
assert(sum_versions(parsePacket(bititerator(test_packet_3))[1]) == 23)
assert(sum_versions(parsePacket(bititerator(test_packet_4))[1]) == 31)

def calculate(parsed_packet):
  id = parsed_packet[1]
  if id == 4:
    return parsed_packet[2]

  subs = []
  for p in parsed_packet[2]:
    subs.append(calculate(p))

  if id == 0:
    print("Sum(" + str(subs) + ") = " + str(sum(subs)))
    return sum(subs)
  elif id == 1:
    print("Prod(" + str(subs) + ") = " + str(math.prod(subs)))
    return math.prod(subs)
  elif id == 2:
    print("Min(" + str(subs) + ") = " + str(min(subs)))
    return min(subs)
  elif id == 3:
    print("Max(" + str(subs) + ") = " + str(max(subs)))
    return max(subs)
  elif id == 5:
    print(str(subs[0]) + " > " + str(subs[1]) + " = " + str(1 if subs[0] > subs[1] else 0))
    return 1 if subs[0] > subs[1] else 0
  elif id == 6:
    print(str(subs[0]) + " < " + str(subs[1]) + " = " + str(1 if subs[0] < subs[1] else 0))
    return 1 if subs[0] < subs[1] else 0
  elif id == 7:
    print(str(subs[0]) + " == " + str(subs[1]) + " = " + str(1 if subs[0] == subs[1] else 0))
    return 1 if subs[0] == subs[1] else 0

test_packet_5 = "C200B40A82"
test_packet_6 = "04005AC33890"
test_packet_7 = "880086C3E88112"
test_packet_8 = "CE00C43D881120"
test_packet_9 = "D8005AC2A8F0"
test_packet_10 = "F600BC2D8F"
test_packet_11 = "9C005AC2F8F0"
test_packet_12 = "9C0141080250320F1802104A08"
assert(calculate(parsePacket(bititerator(test_packet_5))[1]) == 3)
assert(calculate(parsePacket(bititerator(test_packet_6))[1]) == 54)
assert(calculate(parsePacket(bititerator(test_packet_7))[1]) == 7)
assert(calculate(parsePacket(bititerator(test_packet_8))[1]) == 9)
assert(calculate(parsePacket(bititerator(test_packet_9))[1]) == 1)
assert(calculate(parsePacket(bititerator(test_packet_10))[1]) == 0)
assert(calculate(parsePacket(bititerator(test_packet_11))[1]) == 0)
assert(calculate(parsePacket(bititerator(test_packet_12))[1]) == 1)

puzzle_input = "005410C99A9802DA00B43887138F72F4F652CC0159FE05E802B3A572DBBE5AA5F56F6B6A4600FCCAACEA9CE0E1002013A55389B064C0269813952F983595234002DA394615002A47E06C0125CF7B74FE00E6FC470D4C0129260B005E73FCDFC3A5B77BF2FB4E0009C27ECEF293824CC76902B3004F8017A999EC22770412BE2A1004E3DCDFA146D00020670B9C0129A8D79BB7E88926BA401BAD004892BBDEF20D253BE70C53CA5399AB648EBBAAF0BD402B95349201938264C7699C5A0592AF8001E3C09972A949AD4AE2CB3230AC37FC919801F2A7A402978002150E60BC6700043A23C618E20008644782F10C80262F005679A679BE733C3F3005BC01496F60865B39AF8A2478A04017DCBEAB32FA0055E6286D31430300AE7C7E79AE55324CA679F9002239992BC689A8D6FE084012AE73BDFE39EBF186738B33BD9FA91B14CB7785EC01CE4DCE1AE2DCFD7D23098A98411973E30052C012978F7DD089689ACD4A7A80CCEFEB9EC56880485951DB00400010D8A30CA1500021B0D625450700227A30A774B2600ACD56F981E580272AA3319ACC04C015C00AFA4616C63D4DFF289319A9DC401008650927B2232F70784AE0124D65A25FD3A34CC61A6449246986E300425AF873A00CD4401C8A90D60E8803D08A0DC673005E692B000DA85B268E4021D4E41C6802E49AB57D1ED1166AD5F47B4433005F401496867C2B3E7112C0050C20043A17C208B240087425871180C01985D07A22980273247801988803B08A2DC191006A2141289640133E80212C3D2C3F377B09900A53E00900021109623425100723DC6884D3B7CFE1D2C6036D180D053002880BC530025C00F700308096110021C00C001E44C00F001955805A62013D0400B400ED500307400949C00F92972B6BC3F47A96D21C5730047003770004323E44F8B80008441C8F51366F38F240"

print("Answer 1: " + str(sum_versions(parsePacket(bititerator(puzzle_input))[1])))
print("Answer 2: " + str(calculate(parsePacket(bititerator(puzzle_input))[1])))