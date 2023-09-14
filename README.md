[![Python tests](https://github.com/Artemis21/pydis-jam23/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/Artemis21/pydis-jam23/actions/workflows/test.yaml)

# Readable Regexes: Stego Suite

![A screenshot of the app home page, showing a list of codecs to choose from alongside an image of the app logo](https://github.com/Artemis21/pydis-jam23/assets/57376638/bbf37666-b9e6-4701-bf1a-70f6e0a73ec5)

Stego Suite is a toolkit providing a variety of approaches to [steganography](https://en.wikipedia.org/wiki/Steganography), developed as part of [the Python Discord Code Jam, 2023](https://www.pythondiscord.com/events/code-jams/10/).

Watch this [video](https://youtu.be/p08M0LqjWMI) to get an overview of the project.

[The wiki](https://github.com/Artemis21/pydis-jam23/wiki) contains instructions for [installation and development](https://github.com/Artemis21/pydis-jam23/wiki/Installation), [an introductory guide](https://github.com/Artemis21/pydis-jam23/wiki/Guide) and information on [the available codecs](https://github.com/Artemis21/pydis-jam23/wiki/Codecs).

## Quick installation guide:
Make sure you are running at least python3.11.
```shell
git clone https://github.com/Artemis21/pydis-jam23
cd pydis-jam23
pip install hatch
```

## Quick execution guide:
Option 1: Open the GUI:
```shell
hatch run main
```
Option 2: Use the CLI
```shell
hatch run main -h # display the help screen

# command structure for encoding
echo your_message | hatch run main -p input_image --codec_flag [--parameter_flag parameter] > output_image

# command structure for decoding
hatch run main -x input_image --codec_flag [--parameter_flag parameter]
```
Example:
```shell
# encode a message into an image using the ssdb codec
echo your_message | hatch run main -p input_image --ssdb --ssdb-pwd your_password > output_image

# decode it
hatch run main -x image_with_message --ssdb --ssdb-pwd your_password
```
