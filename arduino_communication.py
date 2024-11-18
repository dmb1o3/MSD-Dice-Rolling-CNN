import serial
import os
import time
import ensemble


def extract_jpegs_from_binary(binary_file, output_prefix, output_dir):
    try:
        # Read the binary data from the file
        with open(binary_file, 'rb') as file:
            binary_data = file.read()

        # Define JPEG markers
        start_marker = b'\xFF\xD8'
        end_marker = b'\xFF\xD9'

        start_index = 0
        image_count = 0

        while True:
            # Find the start marker
            start_index = binary_data.find(start_marker, start_index)
            if start_index == -1:
                break

            # Find the end marker
            end_index = binary_data.find(end_marker, start_index)
            if end_index == -1:
                break

            # Extract data between start and end markers (inclusive)
            extracted_data = binary_data[start_index:end_index + 2]

            # Write binary data to a JPEG file
            jpeg_file = f"{output_prefix}_{image_count}.jpg"
            with open(jpeg_file, 'wb') as file:
                file.write(output_dir + extracted_data)

            print(f"JPEG file saved as {jpeg_file}")

            # Move the start index past the current end marker
            start_index = end_index + 2
            image_count += 1

        if image_count == 0:
            print("No JPEG images found in the binary data.")
        else:
            print(f"Extracted {image_count} JPEG images.")


    except Exception as e:
        print(f"An error occurred: {e}")


def read_serial_to_file(port, baud_rate, output_file, output_dir):
    while True:
        try:
            # Open serial port
            ser = serial.Serial(port, baud_rate, timeout=1)
            print(f"Opened serial port {port} at {baud_rate} baud.")

            # Open the output file in append mode
            with open(output_file, 'wb') as file:
                print(f"Writing data to {output_file}... (Press Ctrl+C to stop)")

                while True:
                    try:
                        # Read data from the serial port
                        data = ser.read(ser.in_waiting or 1)  # Read available data
                        if data:
                            file.write(data)  # Write data to file
                            file.flush()  # Ensure data is written to disk immediately

                        time.sleep(0.1)  # Add a small delay to avoid high CPU usage

                    except KeyboardInterrupt:
                        print("Data capture interrupted by user.")
                        break

            print("Data capture complete converting to jpg")
            extract_jpegs_from_binary(output_file, 'image', output_dir)
            print("Running inference on converted image")
            ensemble.setup_run_yolo_ensemble()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            if ser.is_open:
                ser.close()  # Close the serial port
                print(f"Closed serial port {port}.")


def main():
    # Replace with your serial port and baud rate
    # @TODO find way to locate arduino regardless of setup
    # @TODO look into possibly threading so one thread read arduino another runs models
    serial_port = 'COM5'  # e.g., COM3 on Windows or /dev/ttyUSB0 on Linux
    baud_rate = 115200
    output_dir =  os.getcwd() + "/demo/"
    output_file = output_dir + 'output.bin'
    print(output_file)
    read_serial_to_file(serial_port, baud_rate, output_file, output_dir)



if __name__ == "__main__":
    main()