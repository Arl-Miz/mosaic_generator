# Mosaic_generator python application
This is an mosaic generator python application/GUI application that generates mosaic photoos with python and OpenCv and further on the GUI it uses PyQt6

# GUI
## How to use
Run this command on terminal to execute GUI:
```sh
python3 gui.py
```
## Example output

![Screenshot1](assets/Screenshot1.png "Screenshot1")  |  ![Screenshot2](assets/Screenshot2.png "mosaic")|  ![Screenshot3](assets/Screenshot3.png "screenshot3")
:-------------------------:|:-------------------------:|:-------------------------:
  		
# Raw generator
## Requirements
target photo

dataset photos

## How to use
Run this command on terminal to execute raw generator:
```sh
python mosaic.py $block_size $target_image $dataset_path
```
## Example
```sh
python3 mosaic_generator.py 33 assets/wci.jpg assets/cars
```

![Original](assets/wci.jpg "original")  |  ![Mosaic](assets/3_sample_wci_output.png "mosaic")
:-------------------------:|:-------------------------:

Original image (assets/wci.jpg)             |  Mosaic output (assets/3_sample_wci_output.png)
