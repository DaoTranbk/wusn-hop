# #small
# #gaussian
# python scripts/hop_datagen.py -o data -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 40 --num-relay 40 --csize 5 --radius 25,50 --prefix no- --distribution gaussian data/dems_data/*.asc
# #gamma
# python scripts/hop_datagen.py -o data -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 40 --num-relay 40 --csize 5 --radius 25,50 --prefix ga- --distribution gamma data/dems_data/*.asc
# #uniform
# python scripts/hop_datagen.py -o data -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 40 --num-relay 40 --csize 5 --radius 25,50 --prefix uu- --distribution uniform data/dems_data/*.asc

# #small
# #gaussian
# python scripts/hop_datagen.py -o data/medium -W 500 -H 500 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 100 --num-relay 100 --csize 5 --radius 25,50 --prefix no- --distribution gaussian data/dems_data/*.asc
# #gamma
# python scripts/hop_datagen.py -o data/medium -W 500 -H 500 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 100 --num-relay 100 --csize 5 --radius 25,50 --prefix ga- --distribution gamma data/dems_data/*.asc
# #uniform
# python scripts/hop_datagen.py -o data/medium -W 500 -H 500 --depth 1 --height 10 --rows 101 --cols 101 --num-sensor 100 --num-relay 100 --csize 5 --radius 25,50 --prefix uu- --distribution uniform data/dems_data/*.asc

#small
#gaussian
python scripts/hop_datagen.py -o data/extra_small -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 20 --num-relay 20 --csize 5 --radius 25,50 --prefix no- --distribution gaussian data/dems_data/*.asc
#gamma
python scripts/hop_datagen.py -o data/extra_small -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 20 --num-relay 20 --csize 5 --radius 25,50 --prefix ga- --distribution gamma data/dems_data/*.asc
#uniform
python scripts/hop_datagen.py -o data/extra_small -W 200 -H 200 --depth 1 --height 10 --rows 41 --cols 41 --num-sensor 20 --num-relay 20 --csize 5 --radius 25,50 --prefix uu- --distribution uniform data/dems_data/*.asc