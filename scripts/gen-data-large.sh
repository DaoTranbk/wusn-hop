#small
#gaussian
python scripts/hop_datagen.py -o data/large -W 1000 -H 1000 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 200 --num-relay 200 --csize 10 --radius 25 --prefix no- --distribution gaussian data/dems_data/*.asc
#gamma
python scripts/hop_datagen.py -o data/large -W 1000 -H 1000 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 200 --num-relay 200 --csize 10 --radius 25 --prefix ga- --distribution gamma data/dems_data/*.asc
#uniform
python scripts/hop_datagen.py -o data/large -W 1000 -H 1000 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 200 --num-relay 200 --csize 10  --radius 25,50 --prefix uu- --distribution uniform data/dems_data/*.asc