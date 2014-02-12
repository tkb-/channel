"""Channels that process string input.

All channels accept either a single string or a sequence of strings as input.
The output maybe truncated if it becomes unreasonably large.

sum_channel -- outputs the concatenate the strings in the input
delay_channel -- outputs the previous summed input strings 
echo channel -- outputs the summed input concatenated with itself
reverse_channel -- outputs the reverse summed input
process_sequence -- helper function to process a sequence of inputs on a channel

See also modular.channels.channels

"""
from itertools import chain
from modular.channels.channels import shift_channel, memoryless_channel, \
    multi_input_channel

def _sum(value):
    return sum(value)

def sum_channel():
    """Returns an initialized generator that outputs the concatenated strings in the input."""
    return memoryless_channel(_sum)

@multi_input_channel(sum_channel)
def delay_channel():
    """Returns an initialized generator that outputs the previous summed input."""
    return shift_channel(44100)
    
def _inverse(value):
    return - value

@multi_input_channel(sum_channel)
def inverse_channel():
    """Returns an initialized generator that outputs the summed input reversed."""
    return memoryless_channel(_inverse)

def process_sequence(channel, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    raw_outputs = (channel.send(input_) for input_ in inputs)
    
    return (output for output in raw_outputs if output)