import numpy as np
from scipy.special import erfc

def bsc(input_bits, EbN0_dB=1.0, R=1.0):
    """
    Simulates a Binary Symmetric Channel.

    Args:
        input_bits (numpy.ndarray): Array of binary input bits (0s and 1s).
        EbN0_dB (float): Normalized signal to noise ratio in dB.
        R (float): Information rate.

    Returns:
        numpy.ndarray: Array of output bits after passing through the channel.
        p (float): Probability of bit error (0 <= p <= 1).
        
    Author: José Sampaio (08.12.2025)    
    """
    EbN0 = 10**(EbN0_dB/10)
    x = np.sqrt(2*R*EbN0)
    p = 0.5 * erfc(x/np.sqrt(2))
    
    if not (0 <= p <= 1):
        raise ValueError("Error probability 'p' must be between 0 and 1.")

    # Generate random numbers for each bit
    random_numbers = np.random.rand(len(input_bits))

    # Determine which bits to flip based on the error probability
    flip_mask = random_numbers < p

    # Apply the flips: XOR with 1 to flip (0^1=1, 1^1=0)
    output_bits = np.where(flip_mask, 1 - input_bits, input_bits)

    return output_bits, p

