# Homework 1: Substitution-Permutation Network

__Name:__ Xuzheng Lu

__GWid:__ G34363475

***

## 1. Environment and programming language
The algorirhm is written in Python (version = 3.7.4).

***

## 2. Format of the input file

The input file takes the format of `JSON`.

For better readability, the key and the x (or output) takes hexadecimal as input.

```json
{
    "key": "1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c",
    "s-box": {
        "00": "63",
        ...
        "ff": "16"
    }, 
    "permutation function": [
        [0, 0],
        ...
        [31, 31]
    ],
    "m": 128,
    "x (or output)": "3a4b5c6d8e8e996678785299cbfdecab",
    "a": 0 
}
```

#### Description:

__"key":__ string, a 72-digit hexadecimal number (36 bytes)

__"s-box":__ dict, the key is the hexadecimal of the 8 bits input number, and the value is the corresponding hexadecimal number of the output

__"permutation function":__ 2D-list, the first element of each term in the list stands for the index of the input, and the second is the index of the output

__"m":__ int, the length of the input in bits, should be a multiple of 32

__"x (or output)":__ string, a hexadecimal number (m bits) of the input or output

__"a":__ int, value 0 indicates encryption, and value 1 indicates decryption

***

## 3. Configuration
To set up the algorithm, you can modify the code at the end of the `spn.py` file as follows.

```python
SPN(file_path='input_spn.txt', n_rounds=8, save_ouput=True).run()
```

#### Arguments:

__file_path__: str, default='input_spn.txt'. The path of the input file

__n_rounds__: int, default=8. The number of rounds of SPN

__save_ouput__: Boolean, default=True. If True, save the result to 'output_spn.txt'

***

## 4. Run the algorithm
You can run the algorithm by the following command.

```
python spn.py
```

__Notice: If the default version of Python is 2.x, you should use the following command:__

```
python3 spn.py
```

The algorithm will load `input_spn.txt`, and the output will be stored in `output_spn.txt`.

The result will also be displayed in the terminal (shell) as follows.

```shell
--------------------------------------------------------------------------------
Mode        : Encrytion
Key         : 1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c
Input text  : 3a4b5c6d8e8e996678785299cbfdecab
Onput cipher: 4b13ef56dd443a7d052acdb83e1cabcc
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Mode        : Decryption
Key         : 1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c1a2b3c4d5e6f7a8b9c
Input cipher: 4b13ef56dd443a7d052acdb83e1cabcc
Onput text  : 3a4b5c6d8e8e996678785299cbfdecab
--------------------------------------------------------------------------------
```