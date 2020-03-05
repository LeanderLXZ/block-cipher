import json
import numpy as np

class SPN(object):
    
    def __init__(self, 
                 file_path='input_spn.txt', 
                 n_rounds=8,
                 save_ouput=True):
        """Substitution-Permutation Network
        Args:
           file_path : str, default='input_spn.txt'. The path of the input file
           n_rounds  : int, default=8. The number of rounds of SPN
           save_ouput: Boolean, default=True. If True, save the result to 'output_spn.txt'
        """

        # Load input file
        with open(file_path, 'r') as f:
            self.inputs = json.loads(" ".join(line.strip() for line in f))
        
        self.key = self.inputs['key']
        self.s_box= self.inputs['s-box']
        self.p_function = self.inputs['permutation function']
        self.x = self.inputs['x (or output)']
        self.decrypt = self.inputs['a']
        
        # Reversed S-box for decryption
        self.s_box_reverse = {v: k for k, v in self.s_box.items()}
        self.n_rounds = n_rounds
        self.save_ouput = save_ouput

        # Convert hexadecimal inputs to binary
        key_b = self.hex_2_b(self.key)
        self.key = [[int(b) for b in key_b[i:i+32]] for i in range(0, len(key_b), 32)]
        x_b = self.hex_2_b(self.x)
        self.x = [[int(b) for b in x_b[i:i+32]] for i in range(0, len(x_b), 32)]

    def hex_2_b(self, hex_string: str):
        """Convert hexadecimal to binary."""
        return ''.join(['{0:04b}'.format(int(s, 16)) for s in hex_string])

    def b_2_hex(self, b_string: str):
        """Convert binary to hexadecimal."""
        len_string = len(b_string)
        return ''.join(['{:x}'.format(int(b_string[i:i+4], 2)) for i in range(0, len_string, 4)])
    
    def xor(self, x_list: list, k_list: list):
        """Element-wise XOR calculation."""
        cipher = []
        for x_bit, k_bit in zip(x_list, k_list):
            cipher.append(x_bit ^ k_bit)
        return cipher
    
    def s_box_transform(self, input_x: list):
        """Transfrom the input by S-box or reversed S-box."""
        y = []
        x_hex = self.b_2_hex 
        for i in range(0, len(input_x), 8):
            x_part = input_x[i:i+8]
            hex_x_part = self.b_2_hex(''.join([str(x_bit) for x_bit in x_part]))
            # Decryption mode
            if self.decrypt:
                hex_y_part = self.s_box_reverse[hex_x_part]
            # Encryption mode
            else:
                hex_y_part = self.s_box[hex_x_part]
            y_part = [int(b) for b in self.hex_2_b(hex_y_part)]
            y.extend(y_part)
        return y

    def permute(self, input_x: list):
        """Permute bits of the input by permutation function."""
        new_x = np.zeros(len(input_x), dtype=int)
        for i, j in self.p_function:
            # Decryption mode
            if self.decrypt:
                new_x[i] = input_x[j]
            # Encryption mode
            else:
                new_x[j] = input_x[i]
        return new_x
    
    def encrypt_run(self):
        """Encryption."""
        cipher = []
        for x_i in self.x:
            cipher_i = x_i
            for i in range(self.n_rounds):
                # XOR
                cipher_i = self.xor(cipher_i, self.key[i])
                # S-box
                cipher_i = self.s_box_transform(cipher_i)
                if i != self.n_rounds - 1:
                    # Not the last round - Permutation
                    cipher_i = self.permute(cipher_i)
                else:
                    # The last round - XOR
                    cipher_i = self.xor(cipher_i, self.key[-1])
            cipher.extend(cipher_i)
        return cipher
    
    def decrypt_run(self):
        """Decryption."""
        text = []
        for x_i in self.x:
            text_i = x_i
            for i in range(self.n_rounds):
                if i != 0:
                    # The first round - Permutation
                    text_i = self.permute(text_i)
                else:
                    # Not the first round - XOR
                    text_i = self.xor(text_i, self.key[-1])
                # S-box
                text_i = self.s_box_transform(text_i)
                # XOR
                text_i = self.xor(text_i, self.key[-i-2])
            text.extend(text_i)
        return text

    def run(self):
        """Running."""
        # Decryption mode
        if self.decrypt:
            result = self.decrypt_run()
        # Encryption mode
        else:
            result = self.encrypt_run()
        
        # Convert the result from binary to hexadecimal
        result = self.b_2_hex(''.join([str(i) for i in result]))

        # Print out information
        print('-' * 80)
        print('Mode        : {}'.format('Decryption' if self.decrypt else 'Encrytion'))
        print('Key         :', self.inputs['key'])
        print('Input {}:'.format('cipher' if self.decrypt else 'text  '), self.inputs['x (or output)'])
        print('Onput {}:'.format('text  ' if self.decrypt else 'cipher'), result)
        print('-' * 80)

        # Update and save the output file
        if self.save_ouput:
            outputs = self.inputs.copy()
            outputs['x (or output)'] = result
            outputs['a'] = self.decrypt ^ 1
            with open('output_spn.txt', 'w') as f:
                json.dump(outputs, f, indent=4)


if __name__ == '__main__':

    SPN(file_path='input_spn.txt', n_rounds=8, save_ouput=True).run()

    SPN(file_path='output_spn.txt', n_rounds=8, save_ouput=False).run()
