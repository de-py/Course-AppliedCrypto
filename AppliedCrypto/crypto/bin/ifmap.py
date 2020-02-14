#!/Users/daltonellis/Dropbox/SchoolMac/Fall2016/Crypto/AppliedCrypto/crypto/bin/python2.7
"""ifmap - scan for listening DCERPC interfaces

Usage: ifmap.py hostname port

First, this binds to the MGMT interface and gets a list of interface IDs. It
adds to this a large list of interface UUIDs seen in the wild. It then tries to
bind to each interface and reports whether the interface is listed and/or
listening.

This will generate a burst of TCP connections to the given host:port!

Example:
$ ./ifmap.py 10.0.0.30 135
('00000136-0000-0000-C000-000000000046', '0.0'): listed, listening
('000001A0-0000-0000-C000-000000000046', '0.0'): listed, listening
('0B0A6584-9E0F-11CF-A3CF-00805F68CB1B', '1.0'): other version listed, listening
('0B0A6584-9E0F-11CF-A3CF-00805F68CB1B', '1.1'): listed, listening
('1D55B526-C137-46C5-AB79-638F2A68E869', '1.0'): listed, listening
('412F241E-C12A-11CE-ABFF-0020AF6E7A17', '0.0'): other version listed, listening
('412F241E-C12A-11CE-ABFF-0020AF6E7A17', '0.2'): listed, listening
('4D9F4AB8-7D1C-11CF-861E-0020AF6E7C57', '0.0'): listed, listening
('99FCFEC4-5260-101B-BBCB-00AA0021347A', '0.0'): listed, listening
('AFA8BD80-7D8A-11C9-BEF4-08002B102989', '1.0'): not listed, listening
('B9E79E60-3D52-11CE-AAA1-00006901293F', '0.0'): other version listed, listening
('B9E79E60-3D52-11CE-AAA1-00006901293F', '0.2'): listed, listening
('C6F3EE72-CE7E-11D1-B71E-00C04FC3111A', '1.0'): listed, listening
('E1AF8308-5D1F-11C9-91A4-08002B14A0FA', '3.0'): listed, listening
('E60C73E6-88F9-11CF-9AF1-0020AF6E72F4', '2.0'): listed, listening

Usually, only AFA8BD80-...-89, the MGMT interface, is not listed but always
listening on any port. This is imposed by the DCERPC spec.

Author: Catalin Patulea <cat@vv.carleton.ca>
"""
import sys
import struct

from impacket.examples import logger
from impacket import uuid
from impacket.dcerpc.v5.epm import KNOWN_UUIDS
from impacket.dcerpc.v5 import transport, rpcrt, epm
from impacket.dcerpc.v5 import mgmt

uuid_database = set(uuid.string_to_uuidtup(line) for line in """
00000001-0000-0000-c000-000000000046 v0.0
00000131-0000-0000-c000-000000000046 v0.0
00000132-0000-0000-c000-000000000046 v0.0
00000134-0000-0000-c000-000000000046 v0.0
00000136-0000-0000-c000-000000000046 v0.0
00000141-0000-0000-c000-000000000046 v0.0
00000143-0000-0000-c000-000000000046 v0.0
000001a0-0000-0000-c000-000000000046 v0.0
027947e1-d731-11ce-a357-000000000001 v0.0
04fcb220-fcfd-11cd-bec8-00aa0047ae4e v1.0
06bba54a-be05-49f9-b0a0-30f790261023 v1.0
0767a036-0d22-48aa-ba69-b619480f38cb v1.0
0a5a5830-58e0-11ce-a3cc-00aa00607271 v1.0
0a74ef1c-41a4-4e06-83ae-dc74fb1cdd53 v1.0
0b0a6584-9e0f-11cf-a3cf-00805f68cb1b v1.0
0b0a6584-9e0f-11cf-a3cf-00805f68cb1b v1.1
0b6edbfa-4a24-4fc6-8a23-942b1eca65d1 v1.0
0c821d64-a3fc-11d1-bb7a-0080c75e4ec1 v1.0
0d72a7d4-6148-11d1-b4aa-00c04fb66ea0 v1.0
0da5a86c-12c2-4943-30ab-7f74a813d853 v1.0
0e4a0156-dd5d-11d2-8c2f-00c04fb6bcde v1.0
1088a980-eae5-11d0-8d9b-00a02453c337 v1.0
10f24e8e-0fa6-11d2-a910-00c04f990f3b v1.0
11220835-5b26-4d94-ae86-c3e475a809de v1.0
12345678-1234-abcd-ef00-0123456789ab v1.0
12345678-1234-abcd-ef00-01234567cffb v1.0
12345778-1234-abcd-ef00-0123456789ab v0.0
12345778-1234-abcd-ef00-0123456789ac v1.0
12b81e99-f207-4a4c-85d3-77b42f76fd14 v1.0
12d4b7c8-77d5-11d1-8c24-00c04fa3080d v1.0
12e65dd8-887f-41ef-91bf-8d816c42c2e7 v1.0
130ceefb-e466-11d1-b78b-00c04fa32883 v2.0
1453c42c-0fa6-11d2-a910-00c04f990f3b v1.0
1544f5e0-613c-11d1-93df-00c04fd7bd09 v1.0
16e0cf3a-a604-11d0-96b1-00a0c91ece30 v1.0
16e0cf3a-a604-11d0-96b1-00a0c91ece30 v2.0
17fdd703-1827-4e34-79d4-24a55c53bb37 v1.0
18f70770-8e64-11cf-9af1-0020af6e72f4 v0.0
1a9134dd-7b39-45ba-ad88-44d01ca47f28 v1.0
1bddb2a6-c0c3-41be-8703-ddbdf4f0e80a v1.0
1be617c0-31a5-11cf-a7d8-00805f48a135 v3.0
1c1c45ee-4395-11d2-b60b-00104b703efd v0.0
1cbcad78-df0b-4934-b558-87839ea501c9 v0.0
1d55b526-c137-46c5-ab79-638f2a68e869 v1.0
1ff70682-0a51-30e8-076d-740be8cee98b v1.0
201ef99a-7fa0-444c-9399-19ba84f12a1a v1.0
20610036-fa22-11cf-9823-00a0c911e5df v1.0
209bb240-b919-11d1-bbb6-0080c75e4ec1 v1.0
21cd80a2-b305-4f37-9d4c-4534a8d9b568 v0.0
2465e9e0-a873-11d0-930b-00a0c90ab17c v3.0
25952c5d-7976-4aa1-a3cb-c35f7ae79d1b v1.0
266f33b4-c7c1-4bd1-8f52-ddb8f2214ea9 v1.0
28607ff1-15a0-8e03-d670-b89eec8eb047 v1.0
2acb9d68-b434-4b3e-b966-e06b4b3a84cb v1.0
2eb08e3e-639f-4fba-97b1-14f878961076 v1.0
2f59a331-bf7d-48cb-9e5c-7c090d76e8b8 v1.0
2f5f3220-c126-1076-b549-074d078619da v1.2
2f5f6520-ca46-1067-b319-00dd010662da v1.0
2f5f6521-ca47-1068-b319-00dd010662db v1.0
2f5f6521-cb55-1059-b446-00df0bce31db v1.0
2fb92682-6599-42dc-ae13-bd2ca89bd11c v1.0
300f3532-38cc-11d0-a3f0-0020af6b0add v1.2
326731e3-c1c0-4a69-ae20-7d9044a4ea5c v1.0
333a2276-0000-0000-0d00-00809c000000 v3.0
338cd001-2244-31f1-aaaa-900038001003 v1.0
342cfd40-3c6c-11ce-a893-08002b2e9c6d v0.0
3473dd4d-2e88-4006-9cba-22570909dd10 v5.0
3473dd4d-2e88-4006-9cba-22570909dd10 v5.1
359e47c9-682e-11d0-adec-00c04fc2a078 v1.0
367abb81-9844-35f1-ad32-98f038001003 v2.0
369ce4f0-0fdc-11d3-bde8-00c04f8eee78 v1.0
378e52b0-c0a9-11cf-822d-00aa0051e40f v1.0
386ffca4-22f5-4464-b660-be08692d7296 v1.0
38a94e72-a9bc-11d2-8faf-00c04fa378ff v1.0
3919286a-b10c-11d0-9ba8-00c04fd92ef5 v0.0
3ba0ffc0-93fc-11d0-a4ec-00a0c9062910 v1.0
3c4728c5-f0ab-448b-bda1-6ce01eb0a6d5 v1.0
3c4728c5-f0ab-448b-bda1-6ce01eb0a6d6 v1.0
3dde7c30-165d-11d1-ab8f-00805f14db40 v1.0
3f31c91e-2545-4b7b-9311-9529e8bffef6 v1.0
3f77b086-3a17-11d3-9166-00c04f688e28 v1.0
3f99b900-4d87-101b-99b7-aa0004007f07 v1.0
3faf4738-3a21-4307-b46c-fdda9bb8c0d5 v1.0
3faf4738-3a21-4307-b46c-fdda9bb8c0d5 v1.1
41208ee0-e970-11d1-9b9e-00e02c064c39 v1.0
412f241e-c12a-11ce-abff-0020af6e7a17 v0.2
423ec01e-2e35-11d2-b604-00104b703efd v0.0
45776b01-5956-4485-9f80-f428f7d60129 v2.0
45f52c28-7f9f-101a-b52b-08002b2efabe v1.0
469d6ec0-0d87-11ce-b13f-00aa003bac6c v16.0
4825ea41-51e3-4c2a-8406-8f2d2698395f v1.0
4a452661-8290-4b36-8fbe-7f4093a94978 v1.0
4b112204-0e19-11d3-b42b-0000f81feb9f v1.0
4b324fc8-1670-01d3-1278-5a47bf6ee188 v0.0
4b324fc8-1670-01d3-1278-5a47bf6ee188 v3.0
4d9f4ab8-7d1c-11cf-861e-0020af6e7c57 v0.0
4da1c422-943d-11d1-acae-00c04fc2aa3f v1.0
4f82f460-0e21-11cf-909e-00805f48a135 v4.0
4fc742e0-4a10-11cf-8273-00aa004ae673 v3.0
50abc2a4-574d-40b3-9d66-ee4fd5fba076 v5.0
53e75790-d96b-11cd-ba18-08002b2dfead v2.0
56c8504c-4408-40fd-93fc-afd30f10c90d v1.0
57674cd0-5200-11ce-a897-08002b2e9c6d v0.0
57674cd0-5200-11ce-a897-08002b2e9c6d v1.0
5a7b91f8-ff00-11d0-a9b2-00c04fb6e6fc v1.0
5b5b3580-b0e0-11d1-b92d-0060081e87f0 v1.0
5b821720-f63b-11d0-aad2-00c04fc324db v1.0
5c89f409-09cc-101a-89f3-02608c4d2361 v1.1
5ca4a760-ebb1-11cf-8611-00a0245420ed v1.0
5cbe92cb-f4be-45c9-9fc9-33e73e557b20 v1.0
5f54ce7d-5b79-4175-8584-cb65313a0e98 v1.0
6099fc12-3eff-11d0-abd0-00c04fd91a4e v3.0
621dff68-3c39-4c6c-aae3-e68e2c6503ad v1.0
629b9f66-556c-11d1-8dd2-00aa004abd5e v2.0
629b9f66-556c-11d1-8dd2-00aa004abd5e v3.0
63fbe424-2029-11d1-8db8-00aa004abd5e v1.0
654976df-1498-4056-a15e-cb4e87584bd8 v1.0
65a93890-fab9-43a3-b2a5-1e330ac28f11 v2.0
68dcd486-669e-11d1-ab0c-00c04fc2dcd2 v1.0
68dcd486-669e-11d1-ab0c-00c04fc2dcd2 v2.0
69510fa1-2f99-4eeb-a4ff-af259f0f9749 v1.0
6bffd098-0206-0936-4859-199201201157 v1.0
6bffd098-a112-3610-9833-012892020162 v0.0
6bffd098-a112-3610-9833-46c3f874532d v1.0
6bffd098-a112-3610-9833-46c3f87e345a v1.0
6e17aaa0-1a47-11d1-98bd-0000f875292e v2.0
708cca10-9569-11d1-b2a5-0060977d8118 v1.0
70b51430-b6ca-11d0-b9b9-00a0c922e750 v0.0
76d12b80-3467-11d3-91ff-0090272f9ea3 v1.0
76f226c3-ec14-4325-8a99-6a46348418ae v1.0
76f226c3-ec14-4325-8a99-6a46348418af v1.0
77df7a80-f298-11d0-8358-00a024c480a8 v1.0
7af5bbd0-6063-11d1-ae2a-0080c75e4ec1 v0.2
7c44d7d4-31d5-424c-bd5e-2b3e1f323d22 v1.0
7c857801-7381-11cf-884d-00aa004b2e24 v0.0
7e048d38-ac08-4ff1-8e6b-f35dbab88d4a v1.0
7ea70bcf-48af-4f6a-8968-6a440754d5fa v1.0
7f9d11bf-7fb9-436b-a812-b2d50c5d4c03 v1.0
811109bf-a4e1-11d1-ab54-00a0c91e9b45 v1.0
8174bb16-571b-4c38-8386-1102b449044a v1.0
82273fdc-e32a-18c3-3f78-827929dc23ea v0.0
82980780-4b64-11cf-8809-00a004ff3128 v3.0
82ad4280-036b-11cf-972c-00aa006887b0 v2.0
83d72bf0-0d89-11ce-b13f-00aa003bac6c v6.0
83da7c00-e84f-11d2-9807-00c04f8ec850 v2.0
86d35949-83c9-4044-b424-db363231fd0c v1.0
894de0c0-0d55-11d3-a322-00c04fa321a1 v1.0
89742ace-a9ed-11cf-9c0c-08002be7ae86 v2.0
8c7a6de0-788d-11d0-9edf-444553540000 v2.0
8c7daf44-b6dc-11d1-9a4c-0020af6e7c57 v1.0
8cfb5d70-31a4-11cf-a7d8-00805f48a135 v3.0
8d09b37c-9f3a-4ebb-b0a2-4dee7d6ceae9 v1.0
8d0ffe72-d252-11d0-bf8f-00c04fd9126b v1.0
8d9f4e40-a03d-11ce-8f69-08003e30051b v0.0
8d9f4e40-a03d-11ce-8f69-08003e30051b v1.0
8f09f000-b7ed-11ce-bbd2-00001a181cad v0.0
8fb6d884-2388-11d0-8c35-00c04fda2795 v4.1
906b0ce0-c70b-1067-b317-00dd010662da v1.0
91ae6020-9e3c-11cf-8d7c-00aa00c091be v0.0
92bdb7e4-f28b-46a0-b551-45a52bdd5125 v0.0
93149ca2-973b-11d1-8c39-00c04fb984f9 v0.0
93f5ac6f-1a94-4bc5-8d1b-fd44fc255089 v1.0
9556dc99-828c-11cf-a37e-00aa003240c7 v0.0
95958c94-a424-4055-b62b-b7f4d5c47770 v1.0
975201b0-59ca-11d0-a8d5-00a0c90d8051 v1.0
98fe2c90-a542-11d0-a4ef-00a0c9062910 v1.0
99e64010-b032-11d0-97a4-00c04fd6551d v3.0
99fcfec4-5260-101b-bbcb-00aa0021347a v0.0
9b3195fe-d603-43d1-a0d5-9072d7cde122 v1.0
9b8699ae-0e44-47b1-8e7f-86a461d7ecdc v0.0
9e8ee830-4459-11ce-979b-00aa005ffebe v2.0
a002b3a0-c9b7-11d1-ae88-0080c75e4ec1 v1.0
a00c021c-2be2-11d2-b678-0000f87a8f8e v1.0
a0bc4698-b8d7-4330-a28f-7709e18b6108 v4.0
a2d47257-12f7-4beb-8981-0ebfa935c407 v1.0
a398e520-d59a-4bdd-aa7a-3c1e0303a511 v1.0
a3b749b1-e3d0-4967-a521-124055d1c37d v1.0
a4c2fd60-5210-11d1-8fc2-00a024cb6019 v1.0
a4f1db00-ca47-1067-b31e-00dd010662da v1.0
a4f1db00-ca47-1067-b31f-00dd010662da v0.0
a4f1db00-ca47-1067-b31f-00dd010662da v0.81
aa177641-fc9b-41bd-80ff-f964a701596f v1.0
aa411582-9bdf-48fb-b42b-faa1eee33949 v1.0
aae9ac90-ce13-11cf-919e-08002be23c64 v1.0
ae33069b-a2a8-46ee-a235-ddfd339be281 v1.0
afa8bd80-7d8a-11c9-bef4-08002b102989 v1.0
b196b284-bab4-101a-b69c-00aa00341d07 v0.0
b196b286-bab4-101a-b69c-00aa00341d07 v0.0
b58aa02e-2884-4e97-8176-4ee06d794184 v1.0
b7b31df9-d515-11d3-a11c-00105a1f515a v0.0
b97db8b2-4c63-11cf-bff6-08002be23f2f v2.0
b9e79e60-3d52-11ce-aaa1-00006901293f v0.2
bfa951d1-2f0e-11d3-bfd1-00c04fa3490a v1.0
c13d3372-cc20-4449-9b23-8cc8271b3885 v1.0
c33b9f46-2088-4dbc-97e3-6125f127661c v1.0
c681d488-d850-11d0-8c52-00c04fd90f7e v1.0
c6f3ee72-ce7e-11d1-b71e-00c04fc3111a v1.0
c8cb7687-e6d3-11d2-a958-00c04f682e16 v1.0
c9378ff1-16f7-11d0-a0b2-00aa0061426a v1.0
c9ac6db5-82b7-4e55-ae8a-e464ed7b4277 v1.0
ce1334a5-41dd-40ea-881d-64326b23effe v0.2
d049b186-814f-11d1-9a3c-00c04fc9b232 v1.1
d2d79dfa-3400-11d0-b40b-00aa005ff586 v1.0
d335b8f6-cb31-11d0-b0f9-006097ba4e54 v1.5
d3fbb514-0e3b-11cb-8fad-08002b1d29c3 v1.0
d4781cd6-e5d3-44df-ad94-930efe48a887 v0.0
d6d70ef0-0e3b-11cb-acc3-08002b1d29c3 v1.0
d6d70ef0-0e3b-11cb-acc3-08002b1d29c4 v1.0
d7f9e1c0-2247-11d1-ba89-00c04fd91268 v5.0
d95afe70-a6d5-4259-822e-2c84da1ddb0d v1.0
dd490425-5325-4565-b774-7e27d6c09c24 v1.0
e1af8308-5d1f-11c9-91a4-08002b14a0fa v3.0
e248d0b8-bf15-11cf-8c5e-08002bb49649 v2.0
e33c0cc4-0482-101a-bc0c-02608c6ba218 v1.0
e3514235-4b06-11d1-ab04-00c04fc2dcd2 v4.0
e60c73e6-88f9-11cf-9af1-0020af6e72f4 v2.0
e67ab081-9844-3521-9d32-834f038001c0 v1.0
e76ea56d-453f-11cf-bfec-08002be23f2f v2.0
ea0a3165-4834-11d2-a6f8-00c04fa346cc v4.0
eb658b8a-7a64-4ddc-9b8d-a92610db0206 v0.0
ec02cae0-b9e0-11d2-be62-0020afeddf63 v1.0
ecec0d70-a603-11d0-96b1-00a0c91ece30 v1.0
ecec0d70-a603-11d0-96b1-00a0c91ece30 v2.0
eff55e30-4ee2-11ce-a3c9-00aa00607271 v1.0
f309ad18-d86a-11d0-a075-00c04fb68820 v0.0
f50aac00-c7f3-428e-a022-a6b71bfb9d43 v1.0
f5cc59b4-4264-101a-8c59-08002b2f8426 v1.1
f5cc5a18-4264-101a-8c59-08002b2f8426 v56.0
f5cc5a7c-4264-101a-8c59-08002b2f8426 v21.0
f6beaff7-1e19-4fbb-9f8f-b89e2018337c v1.0
f930c514-1215-11d3-99a5-00a0c9b61b04 v1.0
fc13257d-5567-4dea-898d-c6f9c48415a0 v1.0
fd7a0523-dc70-43dd-9b2e-9c5ed48225b1 v1.0
fdb3a030-065f-11d1-bb9b-00a024ea5525 v1.0
ffe561b8-bf15-11cf-8c5e-08002bb49649 v2.0
""".splitlines() if line)
uuid_database = set((uuidstr.upper(), ver) for uuidstr, ver in uuid_database)

# add the ones from ndrutils
k = KNOWN_UUIDS.keys()[0]
def fix_ndr_uuid(ndruuid):
  assert len(ndruuid) == 18
  uuid = ndruuid[:16]
  maj, min = struct.unpack("BB", ndruuid[16:])
  return uuid + struct.pack("<HH", maj, min)
uuid_database.update(
  uuid.bin_to_uuidtup(fix_ndr_uuid(bin)) for bin in KNOWN_UUIDS.keys()
)

def main(args):
  # Init the example's logger theme
  logger.init()
  if len(args) != 2:
    print "usage: ./ifmap.py <host> <port>"
    return 1

  host = args[0]
  port = int(args[1])

  stringbinding = "ncacn_ip_tcp:%s" % host
  trans = transport.DCERPCTransportFactory(stringbinding)
  trans.set_dport(port)

  dce = trans.get_dce_rpc()
  dce.connect()

  dce.bind(mgmt.MSRPC_UUID_MGMT)

  ifids = mgmt.hinq_if_ids(dce)

  uuidtups = set(
    uuid.bin_to_uuidtup(ifids['if_id_vector']['if_id'][index]['Data'].getData())
    for index in range(ifids['if_id_vector']['count'])
  )

  dce.disconnect()

  probes = uuidtups | uuid_database

  for tup in sorted(probes):

    dce.connect()

    binuuid = uuid.uuidtup_to_bin(tup)
    try:
      dce.bind(binuuid)
    except rpcrt.DCERPCException, e:
      if str(e).find('abstract_syntax_not_supported') >= 0:
        listening = False
      else:
        raise
    else:
      listening = True

    listed = tup in uuidtups
    otherversion = any(tup[0] == uuidstr for uuidstr, ver in uuidtups)
    if listed or listening:
      print "%r: %s, %s" % (
        tup,
        "listed" if listed else "other version listed" if otherversion else "not listed",
        "listening" if listening else "not listening"
      )
      if epm.KNOWN_PROTOCOLS.has_key(tup[0]):
          print "Protocol: %s" % (epm.KNOWN_PROTOCOLS[tup[0]])
      else:
          print "Procotol: N/A"

      if KNOWN_UUIDS.has_key(uuid.uuidtup_to_bin(tup)[:18]):
          print "Provider: %s" % (KNOWN_UUIDS[uuid.uuidtup_to_bin(tup)[:18]])
      else:
          print "Provider: N/A"


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
