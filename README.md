# wiifit
Extract Wii Fit weights to a csv file.

# References:
* http://www.kellbot.com/2010/05/extracting-graphing-wii-fit-data/ (the basis of this script)
* http://jansenprice.com/blog?id=9-Extracting-Data-from-Wii-Fit-Plus-Savegame-Files
* http://stackoverflow.com/questions/616249/wii-fit-data-format

# Usage:

1. Download the data from the Wii to an SD card.
2. Build `tachtig`, needed to decrypt the data file.
```sh
sudo apt-get install openssl libssl-dev
git clone git://git.infradead.org/users/segher/wii.git
cd wii
make tachtig
cd ..
```
Ignore the tons of warnings, just as long as it created `tachtig`. Double check with:
```sh
ls -l wii/tachtig
```
3. Install the keys needed to decrypt the file
```sh
mkdir ~/.wii
echo ab01b9d8e1622b08afbad84dbfc2a55d | xxd -r -p - ~/.wii/sd-key
echo 216712e6aa1f689f95c5a22324dc6a98 | xxd -r -p - ~/.wii/sd-iv
echo 0e65378199be4517ab06ec22451a5793 | xxd -r -p - ~/.wii/md5-blanker
```
4. Decrypt it:
```sh
wii/tachtig [SD_CARD/private/wii/title/RFPE/]data.bin
```
That should create a directory like `0001000452465045` with one or more `.dat` files, likely either called `RPHealth.dat` or `FitPlus0.dat`.
5. Extract the contents by running this script:
```sh
./wiifit.py <location of .dat file>
```
6. Do whatever you want with the resulting `wiifit_<name>.csv` file.
