import nfc
import sys

class NFCECHO:
    def __init__(self):
        try:
            self.clf = nfc.ContactlessFrontend('usb')
        except IOError:
            print("Error: NFC reader not found or not accessible.")
            sys.exit(1)
        self.sniffed_data = []

    def on_card_connect(self, tag):
        print("Card detected:")
        print(tag)
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            print("Type3Tag found")
            try:
                sc = nfc.tag.tt3.ServiceCode(0x000B, 0x000B)
                bc = nfc.tag.tt3.BlockCode(0, service=0)
                data = tag.read_without_encryption([sc], [bc])
                self.sniffed_data.append(data)
                print("Data read from the card:")
                print(data)
            except Exception as e:
                print("Error reading card data:", e)
        else:
            print("Unsupported card type")

    def sniff(self):
        print("Waiting for an NFC card... (Press Ctrl+C to stop)")
        try:
            self.clf.connect(rdwr={'on-connect': self.on_card_connect})
        except KeyboardInterrupt:
            print("\nSniffing stopped by user.")

    def replay(self):
        if not self.sniffed_data:
            print("No data to replay")
            return

        print("Replaying captured data...")
        for data in self.sniffed_data:
            print(f"Replaying: {data}")
            # Implement replay logic here, for now, just print the data

    def run(self):
        while True:
            print("\nNFCECHO Menu:")
            print("1. Sniff")
            print("2. Replay")
            print("3. Exit")
            choice = input("Choose an option (1/2/3): ")

            if choice == '1':
                self.sniff()
            elif choice == '2':
                self.replay()
            elif choice == '3':
                self.clf.close()
                print("Exiting NFCECHO. Goodbye!")
                break
            else:
                print("Invalid choice, please enter 1, 2, or 3.")

if __name__ == "__main__":
    nfc_gate = NFCECHO()
    nfc_gate.run()
