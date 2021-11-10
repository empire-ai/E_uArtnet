# E_uArtnet
ESP32 micropython implementation of Art-Net client

# Instalation
Use [thonny](https://thonny.org/)
Open the root folder in thonny and upload the Empire folder like in the screenshot:
![install screenshot](/doc/images/install.png)

# Usage
```python
from Empire.E_uArtnet_client import E_uArtnet_client as ArtNet

def artNetCallback(data_in):
    Print("1st 3 values from ArtNet are: "+str(data_in[0])+", "+str(data_in[1])+", "+(data_in[2]))

ArtNetClientD = ArtNet(artNetCallback)
```

# ToDo
* Implement universes
* Implement max queue
* Implement max callback data array len
* 
