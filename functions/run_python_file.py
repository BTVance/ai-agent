import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    
    try:
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True,timeout=30)

        
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if (not result.stdout ) and (not result.stderr):
            return "No output produced"
        output_parts = []
        if result.stdout:
            output_parts.append("STDOUT: " + result.stdout)
        if result.stderr:   
            output_parts.append("STDERR: " + result.stderr)
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    