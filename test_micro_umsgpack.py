
from umsgpack import loads, dumps

def check_pack(d):
    result = loads(dumps(d))
    if result != d:
        print("Error:\n  expected {}\n  got      {}".format(d, result))
    assert result == d

checks = [
    list(range(10)),
    [1, 'hi', [1,2,3], 42.5],
    {"dict": 8899213, b'awesome': {"pi": 823432, "isfun": "yes"}},
    {("tuple", b'keyed'): [1,2,3,"hi"], 42: "answer"},
]

for c in checks:
    check_pack(c)

print("umsgpack: tests passed")
