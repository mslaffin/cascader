import numpy as np

def read_s2p(filename):
    """Reads a 2-port S-parameter file and returns frequencies and S-parameters in RI format."""
    frequencies = []
    s_params = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            if not line.startswith('!') and line.strip():
                parts = line.split()
                frequencies.append(float(parts[0]))
                # Convert RI format to complex numbers
                s_params_complex = [complex(float(parts[i]), float(parts[i+1])) for i in range(1, 9, 2)]
                s_params.append(s_params_complex)
    return np.array(frequencies), np.array(s_params).reshape(-1, 2, 2)

def cascade_s2p(s1, s2):
    """Cascades two 2-port S-parameter matrices."""
    # Initialize the cascaded S-parameter matrix
    s_cascaded = np.zeros_like(s1)
    for i in range(len(s1)):
        s11 = s1[i][0,0] + (s1[i][0,1] * s1[i][1,0] * s2[i][0,0]) / (1 - s2[i][0,0] * s1[i][1,1])
        s12 = (s1[i][0,1] * s2[i][0,1]) / (1 - s2[i][0,0] * s1[i][1,1])
        s21 = (s2[i][1,0] * s1[i][1,0]) / (1 - s1[i][1,1] * s2[i][0,0])
        s22 = s2[i][1,1] + (s2[i][1,0] * s2[i][0,1] * s1[i][1,1]) / (1 - s1[i][1,1] * s2[i][0,0])
        s_cascaded[i] = np.array([[s11, s12], [s21, s22]])
    return s_cascaded

def write_s2p(filename, frequencies, s_params):
    """Writes frequencies and S-parameters to a .s2p file in RI format."""
    with open(filename, 'w') as file:
        file.write("# Hz S RI R 50\n")
        for freq, s_matrix in zip(frequencies, s_params):
            s_flat = s_matrix.flatten()
            line = f"{freq} " + " ".join(f"{s.real} {s.imag}" for s in s_flat) + "\n"
            file.write(line)

# Example usage
if __name__ == "__main__":
    # Read two S-parameter files
    freqs1, s_params1 = read_s2p('first.s2p')
    freqs2, s_params2 = read_s2p('second.s2p')
    
    # Assuming the frequencies are the same for both files, cascade the S-parameters
    s_cascaded = cascade_s2p(s_params1, s_params2)
    
    # Write the cascaded S-parameters to a new file
    write_s2p('cascaded.s2p', freqs1, s_cascaded)