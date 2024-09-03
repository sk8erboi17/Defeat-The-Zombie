from enum import Enum, auto


class packets(Enum):
    # Define enum members with a byte mark and a message string
    JOIN_PACKET_OUT = (0x01, "join:{0}:{1}:{2}")
    KILL_PACKET_OUT = (0x01, "kill:{0}:{1}")
    MOVEMENT_PACKET_OUT = (0x01, "movement:{0}:{1}:{2}")

    def __init__(self, byte_mark, message):
        self._byte_mark = byte_mark
        self._message = message

    @property
    def byte_mark(self):
        return bytes([self._byte_mark])

    @property
    def message(self):
        return self._message

    def get_combined_message(self):
        """
        Return a combined byte mark and message.
        The byte mark is converted to bytes, and the message is encoded in UTF-8.
        """
        # Combine the byte mark and message
        return bytes([self._byte_mark]) + self._message.encode('utf-8')
