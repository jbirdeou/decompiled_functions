# Import necessary modules
import os
from ghidra.program.model.listing import CodeUnitIterator
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

# Get the current program
current_program = getCurrentProgram()

# Get the program name
program_name = current_program.getName()

# Construct the base output file path
home_dir = os.path.expanduser("~")
base_output_file = os.path.join(home_dir, "Desktop", "{}_decompiled.txt".format(program_name))

# Check if the base output file exists
output_file = base_output_file  # Initialize output_file with base_output_file
file_exists = os.path.isfile(output_file)

file_counter = 1

while file_exists:
    output_file = base_output_file[:-4] + "({})".format(file_counter) + ".txt"
    file_exists = os.path.isfile(output_file)
    file_counter += 1

# Open the output file for writing
with open(output_file, "w") as f:
    # Iterate over all functions in the program
    function_iterator = current_program.getListing().getFunctions(True)
    while function_iterator.hasNext():
        function = function_iterator.next()

        # Get the function name
        function_name = function.getName()

        # Decompile the function
        decompiler = DecompInterface()
        decompiler.openProgram(current_program)
        task_monitor = ConsoleTaskMonitor()
        decompiled_code = decompiler.decompileFunction(function, 0, task_monitor).getDecompiledFunction().getC()

        # Check if the decompiled code is not empty
        if decompiled_code:
            # Write the function name and decompiled code to the output file
            f.write("=" * 85 + "\n\n") # Line separator
            f.write("Function Name: \n\t" + function_name + "\n\n")
            f.write("------Decompiled Code Below------\n\n")
            f.write(decompiled_code)
            f.write("=" * 85 + "\n\n") # Line separator
        else:
            # Write a message indicating that the function is not decompilable
            f.write("## " + function_name + "\n")
            f.write("(Function is not decompilable)\n\n")
            f.write("=" * 85 + "\n\n") # Line separator

    print("Decompiled functions written to " + output_file)
