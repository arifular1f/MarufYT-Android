"""Read-only DEX 035 metadata reader. No VM, instruction rewriting or APK output."""
import hashlib
import struct


class DexError(ValueError):
    pass


class DexReader:
    def __init__(self, data):
        self.data = data
        if len(data) < 112 or data[:8] != b'dex\n035\0':
            raise DexError('Only standard DEX 035 is supported by this reader')
        if self.u32(32) != len(data) or self.u32(36) != 112 or self.u32(40) != 0x12345678:
            raise DexError('Invalid DEX header')
        self.strings = self.table(56, 4)
        self.types = self.table(64, 4)
        self.protos = self.table(72, 12)
        self.fields = self.table(80, 8)
        self.methods = self.table(88, 8)
        self.classes = self.table(96, 32)
        self._strings = {}

    def bounds(self, offset, size):
        if offset < 0 or size < 0 or offset + size > len(self.data):
            raise DexError('DEX offset/size outside input')

    def u32(self, offset):
        self.bounds(offset, 4)
        return struct.unpack_from('<I', self.data, offset)[0]

    def u16(self, offset):
        self.bounds(offset, 2)
        return struct.unpack_from('<H', self.data, offset)[0]

    def table(self, header, width):
        count, offset = self.u32(header), self.u32(header + 4)
        self.bounds(offset, count * width)
        return count, offset

    def index(self, table, index, width):
        if not 0 <= index < table[0]: raise DexError('DEX table index out of range')
        return table[1] + index * width

    def uleb(self, offset):
        value = 0
        for i in range(5):
            self.bounds(offset, 1)
            byte = self.data[offset]
            offset += 1
            if i == 4 and byte > 15: raise DexError('ULEB128 overflow')
            value |= (byte & 127) << (7 * i)
            if byte < 128: return value, offset
        raise DexError('Unterminated ULEB128')

    def string(self, index):
        if index not in self._strings:
            offset = self.u32(self.index(self.strings, index, 4))
            units, offset = self.uleb(offset)
            end = self.data.find(b'\0', offset, min(offset + 1048576, len(self.data)))
            if end < 0: raise DexError('Unterminated/oversized DEX string')
            try:
                value = self.data[offset:end].replace(b'\xc0\x80', b'\0').decode('utf-8', errors='surrogatepass')
                if len(value.encode('utf-16-le', errors='surrogatepass')) // 2 != units:
                    raise DexError('DEX string UTF-16 size mismatch')
                value = value.encode('utf-16-le', errors='surrogatepass').decode('utf-16-le')
            except UnicodeError as exc:
                raise DexError('Invalid modified UTF-8 string') from exc
            self._strings[index] = value
        return self._strings[index]

    def type(self, index):
        return self.string(self.u32(self.index(self.types, index, 4)))

    def type_list(self, offset):
        if not offset: return []
        count = self.u32(offset)
        self.bounds(offset + 4, count * 2)
        return [self.type(self.u16(offset + 4 + 2 * i)) for i in range(count)]

    def method_id(self, index):
        offset = self.index(self.methods, index, 8)
        owner, proto, name = self.u16(offset), self.u16(offset + 2), self.u32(offset + 4)
        p = self.index(self.protos, proto, 12)
        signature = '(' + ''.join(self.type_list(self.u32(p + 8))) + ')' + self.type(self.u32(p + 4))
        return self.type(owner) + '->' + self.string(name) + signature

    def field_id(self, index):
        offset = self.index(self.fields, index, 8)
        return self.type(self.u16(offset)) + '->' + self.string(self.u32(offset + 4)) + ':' + self.type(self.u16(offset + 2))

    def definitions(self):
        for i in range(self.classes[0]):
            offset = self.index(self.classes, i, 32)
            owner = self.type(self.u32(offset))
            parent = self.u32(offset + 8)
            yield {'descriptor': owner, 'class_def_index': i, 'access_flags': self.u32(offset + 4),
                   'superclass': None if parent == 0xffffffff else self.type(parent),
                   'interfaces': self.type_list(self.u32(offset + 12)),
                   'class_data_offset': self.u32(offset + 24)}

    def members(self, definition):
        offset = definition['class_data_offset']
        fields, methods = [], []
        if not offset: return fields, methods
        counts = []
        for _ in range(4):
            count, offset = self.uleb(offset)
            counts.append(count)
        if sum(counts) > 1000000: raise DexError('Class member limit exceeded')
        for count, kind in zip(counts[:2], ('static', 'instance')):
            index = 0
            for _ in range(count):
                delta, offset = self.uleb(offset)
                flags, offset = self.uleb(offset)
                index += delta
                fields.append({'identifier': self.field_id(index), 'kind': kind, 'access_flags': flags})
        for count, kind in zip(counts[2:], ('direct', 'virtual')):
            index = 0
            for _ in range(count):
                delta, offset = self.uleb(offset)
                flags, offset = self.uleb(offset)
                code, offset = self.uleb(offset)
                index += delta
                item = {'identifier': self.method_id(index), 'kind': kind, 'access_flags': flags,
                        'method_id_index': index, 'code_offset': code,
                        'instruction_units': 0, 'instruction_sha256': None}
                if code:
                    units = self.u32(code + 12)
                    self.bounds(code + 16, units * 2)
                    item['instruction_units'] = units
                    item['instruction_sha256'] = hashlib.sha256(self.data[code + 16:code + 16 + units * 2]).hexdigest()
                methods.append(item)
        owner = definition['descriptor'] + '->'
        if any(not item['identifier'].startswith(owner) for item in fields + methods):
            raise DexError('Class data member owner mismatch')
        return fields, methods
