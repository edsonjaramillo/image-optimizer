from enum import Enum
from math import pow


class ByteRanges(Enum):
    BYTE = 1
    KB = pow(1024, 1)
    MB = pow(1024, 2)
    GB = pow(1024, 3)
    TB = pow(1024, 4)
    PB = pow(1024, 5)


class BytesConverter:
    """Bytes Converter is a class that converts bytes to a specified unit or the largest unit."""

    def convert(self, bytes: int, to: ByteRanges, decimals=3) -> float:
        """Convert bytes to a specified unit.
        Arguments:
            `bytes` (int): The number of bytes to convert.
            `to` (ByteRanges): The unit to convert to.
            Ex: `ByteRanges.KB` | `ByteRanges.MB` | `ByteRanges.GB` | `ByteRanges.TB` | `ByteRanges.PB`"""
        converted_bytes = bytes / to.value
        return round(converted_bytes, decimals)

    def convert_to_largest(self, bytes: int) -> str:
        """Convert bytes to the largest unit.
        Arguments:
            `bytes` (int): The number of bytes to convert."""
        if bytes >= ByteRanges.BYTE.value and bytes < ByteRanges.KB.value:
            return f"{self.convert(bytes, ByteRanges.BYTE)} B"
        elif bytes >= ByteRanges.KB.value and bytes < ByteRanges.MB.value:
            return f"{self.convert(bytes, ByteRanges.KB)} KB"
        elif bytes >= ByteRanges.MB.value and bytes < ByteRanges.GB.value:
            return f"{self.convert(bytes, ByteRanges.MB)} MB"
        elif bytes >= ByteRanges.GB.value and bytes < ByteRanges.TB.value:
            return f"{self.convert(bytes, ByteRanges.GB)} GB"
        elif bytes >= ByteRanges.TB.value and bytes < ByteRanges.PB.value:
            return f"{self.convert(bytes, ByteRanges.TB)} TB"
        elif bytes >= ByteRanges.PB.value:
            return f"{self.convert(bytes, ByteRanges.PB)} PB"
