from stem.proto_list import ProtoList

if __name__ == '__main__':
    with ProtoList('/home/daniil/advanced-python-homework/stem_framework/tests/test_proto_list', 'saad') as r:
        print(r)
    # a = int.from_bytes(b'\x00\x00\x00\x00\x00\x00\x00\x04', "big")
    # print(a)
    # s = str.encode('q' * a)
    # with open('/home/daniil/advanced-python-homework/stem_framework/tests/test_proto_list', 'wb') as f:
    #     f.write(b'\x00\x00\x00\x00\x00\x00\x00\x04' + s)
