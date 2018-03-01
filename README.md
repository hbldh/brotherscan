# Brother Scanner

## Usage

```bash
$ python scan.py ~/Scan --prefix=WTF --device="brother4:net1;dev0" -t 8
Will use: 'brother4:net1;dev0' (Unknown, Unknown, Unknown)
Scanning /home/hbldh/Scan/WTF_001.pdf...
100%|██████████| 3472/3472 [00:14<00:00, 59.16it/s] 
Sleeping...: 100%|██████████| 80/80 [00:08<00:00,  9.95it/s]
Scanning /home/hbldh/Scan/WTF_002.pdf...
100%|██████████| 3472/3472 [00:05<00:00, 633.01it/s]
Sleeping...:  46%|████▋     | 37/80 [00:03<00:04,  9.95it/s]
```

Will keep scanning indefinitely until killed by `KeyboardInterrupt`. 

## Linux
Brother Driver, Linux:
http://support.brother.com/g/s/id/linux/en/download_scn.html#brscan4

Find IP of your printer, and configure it with Brother's `brsaneconfig4` tool.
```bash
brsaneconfig4 -a name=DCPJ725DW model=DCP-J725DW ip=192.168.1.234
```

This will allow `pyinsane2` to find it when scanning network for devices.
