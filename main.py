import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QComboBox, QMessageBox, QFileDialog, QHBoxLayout)
from PySide6.QtWidgets import QStatusBar

DEFAULT_VENDOR = bytes.fromhex(
    "30 03 56 00 49 00 41 00 20 00 4C 00 61 00 62 00 73 00 2C 00 20 00 49 00 6E 00 63 00 2E 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00"
)
DEFAULT_SERIAL = bytes.fromhex(
    "14 03 30 00 30 00 30 00 30 00 30 00 30 00 30 00 30 00 31 00"
)
DEFAULT_U3HUB = bytes.fromhex(
    "30 03 55 00 53 00 42 00 33 00 2E 00 31 00 20 00 48 00 75 00 62 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00"
)
DEFAULT_U2HUB = bytes.fromhex(
    "30 03 55 00 53 00 42 00 32 00 2E 00 30 00 20 00 48 00 75 00 62 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00 20 00"
)

def to_usb_string_descriptor(text, total_bytes, fill_char=b'\x20\x00'):
    encoded = text.encode('utf-16le')
    if len(encoded) > total_bytes - 2:
        encoded = encoded[:total_bytes-2]
    padding_len = total_bytes - 2 - len(encoded)
    if fill_char:
        padding = fill_char * (padding_len // 2)
    else:
        padding = b''
    length_byte = total_bytes.to_bytes(1, 'little')
    type_byte = b'\x03'
    return length_byte + type_byte + encoded + padding

def decode_usb_descriptor(data):
    text_bytes = data[2:]
    text = text_bytes.decode('utf-16le', errors='ignore').rstrip()
    return text

class USBEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VL822 Firmware Descriptor Editor")

        self.max_lengths = {
            "vendor": 48,
            "serial": len(DEFAULT_SERIAL),
            "u3": 48,
            "u2": 48
        }

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Firmware File:"))
        self.bin_selector = QComboBox()
        self.refresh_bin_files()
        layout.addWidget(self.bin_selector)

        self.vendor_input, self.vendor_remain = self.create_labeled_input("Vendor:", decode_usb_descriptor(DEFAULT_VENDOR), "vendor", layout)
        self.serial_input, self.serial_remain = self.create_labeled_input("Serial Number:", decode_usb_descriptor(DEFAULT_SERIAL), "serial", layout)
        self.u3_input, self.u3_remain = self.create_labeled_input("U3 Hub Name:", decode_usb_descriptor(DEFAULT_U3HUB), "u3", layout)
        self.u2_input, self.u2_remain = self.create_labeled_input("U2 Hub Name:", decode_usb_descriptor(DEFAULT_U2HUB), "u2", layout)

        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.execute)
        layout.addWidget(self.execute_btn)
        
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Powered by barryblueice, 2025")
        layout.addWidget(self.status_bar)


        self.setLayout(layout)

    def refresh_bin_files(self):
        self.bin_selector.clear()
        bin_dir = os.path.join(os.getcwd(), "BinFile")
        if os.path.exists(bin_dir):
            bins = [f for f in os.listdir(bin_dir) if f.lower().endswith(".bin")]
            self.bin_selector.addItems(bins)

    def create_labeled_input(self, label_text, default_text, key, parent_layout):
        label = QLabel(label_text)
        input_box = QLineEdit()
        input_box.setText(default_text)
        remain_label = QLabel()
        parent_layout.addWidget(label)
        parent_layout.addWidget(input_box)
        parent_layout.addWidget(remain_label)
        self.update_remaining_label(input_box, remain_label, key)

        input_box.textChanged.connect(lambda text: self.on_text_changed(text, input_box, remain_label, key))
        return input_box, remain_label

    def update_remaining_label(self, input_box, label, key):
        used_bytes = len(input_box.text().encode('utf-16le'))
        max_bytes = self.max_lengths[key] - 2
        remaining_chars = (max_bytes - used_bytes) // 2
        if remaining_chars < 0:
            remaining_chars = 0
        label.setText(f"Remaining characters: {remaining_chars}")

    def on_text_changed(self, text, input_box, label, key):
        max_bytes = self.max_lengths[key] - 2
        encoded = text.encode('utf-16le')
        if len(encoded) > max_bytes:

            truncated = ""
            for ch in text:
                if len((truncated + ch).encode('utf-16le')) > max_bytes:
                    break
                truncated += ch
            input_box.blockSignals(True)
            input_box.setText(truncated)
            input_box.blockSignals(False)
        self.update_remaining_label(input_box, label, key)

    def execute(self):

        vendor_bytes = to_usb_string_descriptor(self.vendor_input.text(), 48)

        fill_char = b'\x30\x00'
        serial_bytes = to_usb_string_descriptor(self.serial_input.text(), len(DEFAULT_SERIAL), fill_char)
        u3_bytes = to_usb_string_descriptor(self.u3_input.text(), 48)
        u2_bytes = to_usb_string_descriptor(self.u2_input.text(), 48)

        selected_bin = self.bin_selector.currentText()
        if not selected_bin:
            QMessageBox.warning(self, "Error", "No Firmware file selected")
            return
        bin_path = os.path.join(os.getcwd(), "BinFile", selected_bin)
        if not os.path.exists(bin_path):
            QMessageBox.warning(self, "Error", f"{selected_bin} not found")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Modified Firmware", selected_bin, "Binary Files (*.bin)")
        if not save_path:
            return

        with open(bin_path, "rb") as f:
            data = f.read()

        data = data.replace(DEFAULT_VENDOR, vendor_bytes)
        data = data.replace(DEFAULT_SERIAL, serial_bytes)
        data = data.replace(DEFAULT_U3HUB, u3_bytes)
        data = data.replace(DEFAULT_U2HUB, u2_bytes)

        with open(save_path, "wb") as f:
            f.write(data)

        QMessageBox.information(self, "Success", f"Modified Firmware saved to:\n{save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = USBEditor()
    window.show()
    sys.exit(app.exec())
