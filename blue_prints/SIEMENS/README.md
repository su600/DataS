# Siemens PLC Integration

This module provides integration with Siemens PLCs using the python-snap7 library.

## Features

- Connect to Siemens S7 PLCs (S7-300, S7-400, S7-1200, S7-1500)
- Read multiple variables from PLC
- Support for various data types: Bool, Real, Int, Dword, String
- Automatic batching for reading more than 20 variables

## Reading Multiple Variables

### Batch Reading for Large Variable Lists

The `read_multi_vars()` function in python-snap7 has a limitation of approximately 20 variables per call. When you need to read more than 20 variables, the code automatically splits the request into batches of 20.

**Example:**
- If you have 45 variables to read:
  - Batch 1: Variables 0-19 (20 variables)
  - Batch 2: Variables 20-39 (20 variables)
  - Batch 3: Variables 40-44 (5 variables)

This batching is handled automatically by the `s7_multi_read()` function.

### Usage

1. Upload an Excel file with your variable list containing:
   - Name: Variable name
   - Data Type: Bool, Real, Int, Dword, or String
   - Logical Address: Variable address (e.g., I1.0, Q2.3, M10.5)

2. The system will:
   - Parse the Excel file
   - Connect to the PLC
   - Read all variables (automatically batching if > 20 variables)
   - Return results as a dictionary

### Important Notes

- **Batch Size:** Default batch size is 20 variables per read operation
- **Performance:** Reading 100 variables will require 5 separate read operations
- **Error Handling:** Each batch is read independently; if one batch fails, it won't affect the others
- **Data Types:** Ensure the data type in your Excel matches the actual PLC data type

## Configuration

Connect to PLC using:
- IP Address: PLC IP address on the network
- Rack: CPU rack number (typically 0)
- Slot: CPU slot number (typically 1 for S7-300/400, 0 for S7-1200/1500)

## Troubleshooting

### "Error reading variables" when reading > 20 variables
This issue has been fixed by implementing automatic batching. If you still encounter this error, verify that:
- Your PLC is accessible on the network
- The variable addresses in your Excel file are correct
- The data types match the PLC configuration

### Connection timeout
- Verify network connectivity to PLC
- Check firewall settings
- Ensure the PLC allows external connections

## Technical Details

The batching implementation:
1. Determines total number of variables
2. If ≤ 20: reads all at once
3. If > 20: 
   - Calculates number of batches needed
   - Creates batch arrays of maximum 20 items
   - Reads each batch sequentially
   - Combines results into final dataset

## References

- [python-snap7 Documentation](https://python-snap7.readthedocs.io/)
- [Snap7 Library](http://snap7.sourceforge.net/)
- [Issue #155: How to use read_multi_vars() when variables is more than 20?](https://github.com/su600/DataS/issues/155)
