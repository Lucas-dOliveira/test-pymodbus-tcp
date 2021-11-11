import sys

from pymodbus.client.sync import ModbusTcpClient


class ModbusMasterTest:
    def __init__(self, ip_address, port):
        self._ip_address = ip_address
        self._port = port
        self.client = ModbusTcpClient(host=ip_address, port=port)

    def write_coil(self):
        address = int(input("Writing coil - Enter address: "))
        value = int(input("Writing coil - Enter Value: "))

        response = self.client.write_coil(address, value)
        print(f"\n# RESPONSE: Wrote coil: {response}\n")

    def read_coils(self):
        starting_address = int(input("Reading coils - Enter starting address: "))
        quantity = int(input("Reading coils - Enter the number of coils to read: "))

        slave_unity = input("Slave unit target (None)")
        if slave_unity:
            result = self.client.read_coils(
                starting_address, quantity, unit=int(slave_unity)
            )
        else:
            result = self.client.read_coils(starting_address, quantity)

        print(f"\n# RESPONSE: Received coil bits: {result.bits[0:quantity]}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    assert len(args) == 2, "main [ip_address] [port]"

    ip_address, port = args
    master = ModbusMasterTest(ip_address, port)

    options = [
        ("Write coil", master.write_coil),
        ("Read coils", master.read_coils),
        ("Exit", sys.exit),
    ]

    while True:
        for index, value in enumerate(options):
            option_text = value[0]
            print(f"{index + 1} - {option_text}")
        selected_option = int(input("\nSelect: "))
        if selected_option > len(options):
            continue
        selected_function = options[selected_option - 1][1]
        selected_function()
