import re
import os

def read_file(spectra_file):
    file = open(spectra_file, 'r')
    spec = file.readlines()
    file.close()
    return spec

def make_directories_if_needed(output_filename):
    directory_path = os.path.dirname(output_filename)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def write_file(spec, output_filename):
    output_filename = re.sub(r"\\", "/", output_filename)
    make_directories_if_needed(output_filename)
    output = ''.join(spec)
    file = open(output_filename, 'w', newline='\n')
    file.write(output)
    file.close()

def interpolation_spec(spec):
    spec = [re.sub(r"alw\s*\(([^\)]*)\)", r"G (\1)", line) for line in spec]
    spec = [re.sub(r"alwEv\s*\(([^\)]*)\)", r"GF (\1)", line) for line in spec]
    spec = [re.sub(r"GF\s*\(([^\)]*)\)", r"G(F(\1))", line) for line in spec]
    spec = [re.sub(r"next\(([^\)]*)\)", r"X(\1)", line) for line in spec]
    spec = [re.sub(r'(\w+)=true', r'\1', x) for x in spec]
    spec = [re.sub(r'(\w+)=false', r'!\1', x) for x in spec]
    spec = [re.sub(";", "", line) for line in spec]
    return spec


def main():
    spec = read_file("Lift.spectra")
    print("=== SPECTRA SPEC ===")
    print(''.join(spec))
    spec = interpolation_spec(spec)
    print("=== INTERPOLATION SPEC ===")
    print(''.join(spec))

if __name__=="__main__":
    main()